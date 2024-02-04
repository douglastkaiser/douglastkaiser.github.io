// bayesian.test.js
const bayesianAverage = require('./bayesian');

describe('Bayesian Average Function', () => {
    test('returns correct Bayesian average for non-zero values', () => {
        const averageRating = 3; // System average rating
        const totalVotes = 50; // Total votes in the system
        expect(bayesianAverage(4, 100, averageRating, totalVotes)).toBeCloseTo(3.92, 2);
        expect(bayesianAverage(5, 50, averageRating, totalVotes)).toBeCloseTo(4.0, 2);
    });

    test('returns system average rating when item has no votes', () => {
        const averageRating = 3;
        const totalVotes = 50;
        expect(bayesianAverage(0, 0, averageRating, totalVotes)).toBe(averageRating);
    });
});
