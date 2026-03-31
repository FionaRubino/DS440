/**
 * Calculates a Health Score for the Web App UI
 * @param {Object} recipe - {calories, protein, fat, sodium, carbs}
 * @returns {Number} - Score from 0 to 100
 */
function getNutriScore(recipe) {
    const { calories, protein, fat, sodium, carbs } = recipe;

    if (!calories || calories <= 0) return 0;

    let score = 60;

    // 1. Protein Bonus (Goal: High Protein Density)
    const pPerc = (protein * 4 / calories) * 100;
    score += (pPerc * 1.5);

    // 2. Sodium Penalty (Goal: < 1mg per calorie)
    const sDensity = sodium / calories;
    score -= (sDensity * 15);

    // 3. Fat Penalty (Goal: < 35% calories from fat)
    const fPerc = (fat * 9 / calories) * 100;
    if (fPerc > 35) {
        score -= (fPerc - 35);
    }

    // 4. Carb Balance (Goal: < 60% calories from carbs)
    const cPerc = (carbs * 4 / calories) * 100;
    if (cPerc > 60) {
        score -= (cPerc - 60);
    }

    // Return final rounded score between 0 and 100
    return Math.min(100, Math.max(0, Math.round(score * 10) / 10));
}

// Example usage:
const sampleRecipe = { calories: 555, protein: 67, fat: 15, sodium: 1150, carbs: 37 };
console.log(`Health Score: ${getNutriScore(sampleRecipe)}`);