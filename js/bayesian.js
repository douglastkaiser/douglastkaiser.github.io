
function bayesianAverage(rating, n_votes, globalaverageRating, global_n_Votes) {
    return ((n_votes * rating) + (global_n_Votes * globalaverageRating)) / (n_votes + global_n_Votes);
}

function compareRatings() {
    // Clear output.
    document.getElementById('bayesian_result').innerText = ''
    document.getElementById('bayesian_compare_result').innerText = ''

    // Assuming a mid-point average rating for the whole system
    const globalaverageRating = parseFloat(document.getElementById('globalaverageRating').value) || 3.5;
    // Assuming a baseline number of total n_votes for normalization
    const global_n_Votes = parseFloat(document.getElementById('global_n_Votes').value) || 50;

    const rating1 = parseFloat(document.getElementById('rating1').value);
    const n_votes1 = parseInt(document.getElementById('n_votes1').value);
    const rating2 = parseFloat(document.getElementById('rating2').value);
    const n_votes2 = parseInt(document.getElementById('n_votes2').value);

    // Protection
    // Required fields required.
    if (isNaN(rating1) || isNaN(n_votes1) || isNaN(rating2) || isNaN(n_votes2)) {
        document.getElementById('bayesian_result').innerText = 'Required field missing.'
        return;
    }
    // non zero n votes needed.
    if ((n_votes1 == 0) || (n_votes2 == 0)) {
        document.getElementById('bayesian_result').innerText = 'Non-zero number of n_votes required.'
        return;
    }

    const bayesian1 = bayesianAverage(rating1, n_votes1, globalaverageRating, global_n_Votes);
    const bayesian2 = bayesianAverage(rating2, n_votes2, globalaverageRating, global_n_Votes);

    document.getElementById('bayesian_result').innerText = `Item 1: Bayesian Average = ${bayesian1.toFixed(2)}\nItem 2: Bayesian Average = ${bayesian2.toFixed(2)}`;
    
    resultText = ''
    if (bayesian1 > bayesian2) {
        resultText += 'Item 1 has a stronger score.';
    } else if (bayesian2 > bayesian1) {
        resultText += 'Item 2 has a stronger score.';
    } else {
        resultText += 'Both items have equal scores.';
    }

    document.getElementById('bayesian_compare_result').innerText = resultText;
    
}
