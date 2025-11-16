import { VERSION } from "./version.js";

export function initializeUI(root = document) {
  if (typeof $ === "undefined") {
    return;
  }
  const tableEl = root.querySelector("#exerciseTable");
  const dropdownEl = root.querySelector("#exerciseDropdown");
  if (!tableEl || !dropdownEl) {
    return;
  }

  // Check if DataTable is already initialized to prevent reinitialization error
  const table = ($.fn.DataTable && $.fn.DataTable.isDataTable(tableEl))
    ? $(tableEl).DataTable()
    : $(tableEl).DataTable({ responsive: true });
  $(dropdownEl)
    .select2({ placeholder: "Filter by Exercise", allowClear: true })
    .on("change", function () {
      const val = $.fn.dataTable.util.escapeRegex($(this).val());
      table.column(0).search(val ? "^" + val + "$" : "", true, false).draw();
      $(".exercise-figure").hide();
      const figId = $(this).find("option:selected").data("fig");
      if (figId) {
        $("#fig-" + figId).show();
      }
    });
}

async function fetchWheel(doc) {
  const bases = [];
  try {
    bases.push(new URL(import.meta.url));
  } catch (_) {}
  if (doc?.baseURI) {
    bases.push(new URL(doc.baseURI));
  }

  const names = [
    "kaiserlift.whl",
    `kaiserlift-${VERSION}-py3-none-any.whl`,
    "dist/kaiserlift.whl",
    `dist/kaiserlift-${VERSION}-py3-none-any.whl`,
  ];

  const candidates = [];
  for (const base of bases) {
    for (const name of names) {
      candidates.push(new URL(name, base));
    }
  }

  for (const url of candidates) {
    try {
      const response = await fetch(url);
      if (response.ok) {
        return { response, url: url.href };
      }
      console.error(`Wheel fetch returned ${response.status} at ${url.href}`);
    } catch (err) {
      console.error("Failed to fetch Pyodide wheel", url.href, err);
    }
  }
  console.error(
    "Failed to fetch wheel from known locations: " +
      candidates.map((u) => u.href).join(", "),
  );
  return null;
}

export async function init(loadPyodide, doc = document) {
  const result = doc.getElementById("result");

  // Ensure the initial UI is usable even if Pyodide fails to load.
  initializeUI(doc);

  const cachedHtml = localStorage.getItem("kaiserliftHtml");
  if (cachedHtml) {
    result.innerHTML = cachedHtml;
    initializeUI(result);
  }

  try {
    const loader =
      loadPyodide ??
      (await import(
        "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.mjs"
      )).loadPyodide;
    const pyodide = await loader();
    await pyodide.loadPackage(["pandas", "numpy", "matplotlib", "micropip"]);

    const wheel = await fetchWheel(doc);
    try {
      if (wheel) {
        const data = new Uint8Array(await wheel.response.arrayBuffer());
        const wheelName = wheel.url.split("/").pop();
        pyodide.FS.writeFile(wheelName, data);
        await pyodide.runPythonAsync(`
import micropip
await micropip.install('${wheelName}')
`);
      } else {
        console.warn("Falling back to installing kaiserlift from PyPI");
        await pyodide.runPythonAsync(`
import micropip
await micropip.install('kaiserlift')
`);
      }
    } catch (err) {
      console.error("Failed to install kaiserlift", err);
      throw err;
    }

    const fileInput = doc.getElementById("csvFile");
    const uploadButton = doc.getElementById("uploadButton");
    const progressBar = doc.getElementById("uploadProgress");
    const clearButton = doc.getElementById("clearButton");

    if (clearButton) {
      clearButton.addEventListener("click", () => {
        localStorage.removeItem("kaiserliftCsv");
        localStorage.removeItem("kaiserliftHtml");
        result.innerHTML = "";
      });
    }

    uploadButton.addEventListener("click", async () => {
      const file = fileInput.files?.[0];
      if (!file) {
        showError("No file selected", "Please select a CSV file to upload.");
        return;
      }

      // Validate file type
      if (!file.name.endsWith('.csv')) {
        showError("Invalid file type", "Please upload a CSV file. Selected file: " + file.name);
        return;
      }

      let progressInterval;
      let advance = () => {};
      if (progressBar) {
        progressBar.style.display = "block";
        progressBar.value = 0;
        let targetProgress = 0;
        advance = (val) => {
          if (val > targetProgress) targetProgress = val;
        };
        progressInterval = setInterval(() => {
          if (progressBar.value < Math.min(targetProgress, 90)) {
            progressBar.value += 1;
          }
        }, 100);
        advance(10);
      }

      try {
        const text = await file.text();
        advance(25);

        // Validate CSV format
        if (!text.includes('Date') || !text.includes('Exercise')) {
          throw new Error('Invalid CSV format. Please ensure your CSV contains "Date" and "Exercise" columns. Use FitNotes export format.');
        }

        pyodide.globals.set("csv_text", text);
        advance(50);
        advance(75);
        const html = await pyodide.runPythonAsync(`
          import io
          from kaiserlift.pipeline import pipeline
          buffer = io.StringIO(csv_text)
          pipeline([buffer], embed_assets=False)
        `);
        result.innerHTML = "";
        result.innerHTML = html;
        localStorage.setItem("kaiserliftCsv", text);
        localStorage.setItem("kaiserliftHtml", html);
        initializeUI(result);
        if (progressBar) {
          advance(90);
          await new Promise((resolve) => {
            const wait = setInterval(() => {
              if (progressBar.value >= 90) {
                clearInterval(wait);
                resolve();
              }
            }, 50);
          });
          if (progressInterval) clearInterval(progressInterval);
          progressBar.value = 100;
        }
      } catch (err) {
        console.error(err);
        showError("Processing Failed", getErrorMessage(err));
      } finally {
        if (progressInterval) clearInterval(progressInterval);
        pyodide.globals.delete("csv_text");
        if (progressBar) progressBar.style.display = "none";
      }
    });

    function getErrorMessage(err) {
      const errorStr = err.toString();

      if (errorStr.includes('KeyError') || errorStr.includes('columns')) {
        return `Missing required columns in CSV. Please ensure your CSV has these columns: Date, Exercise, Category, Weight, Reps.

Expected format:
Date,Exercise,Category,Weight,Reps
2022-09-14,Bench Press,Chest,135.0,10

Error details: ${errorStr}`;
      }

      if (errorStr.includes('Invalid CSV format')) {
        return err.message + `

Expected CSV format:
Date,Exercise,Category,Weight,Reps
2022-09-14,Flat Barbell Bench Press,Chest,45.0,10
2022-09-14,Dumbbell Curl,Biceps,35.0,10`;
      }

      return `Failed to process CSV: ${errorStr}

Common issues:
• CSV is missing required columns (Date, Exercise, Category, Weight, Reps)
• Data format is incorrect
• File is corrupted or empty

Please check your CSV file and try again.`;
    }

    function showError(title, message) {
      result.innerHTML = `
        <div style="
          background: #fee;
          border: 2px solid #fcc;
          border-radius: 8px;
          padding: 20px;
          margin: 20px 0;
          text-align: left;
          max-width: 600px;
        ">
          <h3 style="color: #c00; margin-top: 0;">❌ ${title}</h3>
          <pre style="
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: monospace;
            font-size: 0.9em;
            color: #333;
          ">${message}</pre>
        </div>
      `;
    }
  } catch (err) {
    console.error(err);
    result.textContent = "Failed to initialize Pyodide: " + err;
  }
}

if (typeof window !== "undefined") {
  init().catch((err) => console.error(err));
}
