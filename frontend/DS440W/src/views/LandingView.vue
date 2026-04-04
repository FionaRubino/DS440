<template>
    <v-container fluid class="align center -height d-flex flex-column">

      <!-- TITLE -->
      <div class="main-title">
          <img
            src="https://th.bing.com/th/id/OIP.1axdzj_b8TA5WMqnvJKx7gHaFj?w=256&h=192&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3"
            alt="PSU Logo"
            class="psu-logo"
          />
          <h1 class="main-title">State College Nutrition Tracker</h1>
        </div>

      <!-- RECIPE TABS -->
      <div style="max-width: 1200px; width: 100%; margin: 0 auto;">
        <v-tabs
          v-model="selectedTab"
          color="primary"
          show-arrows
      >
          <v-tab
            v-for="(recipe, index) in recipes"
              :key="recipe.name"
          >
              {{ recipe.name }}
          </v-tab>
      </v-tabs>
    </div>

      <!-- RECIPE CONTENT -->
      <v-window v-model="selectedTab" class="mt-6">

        <v-window-item
          v-for="(recipe, index) in recipes"
          :key="recipe.name"
        >

          <v-card class="pa-6">

            <h2 class="text-center mb-4">{{ recipe.name }}

            </h2>

            <!-- SUB TABS -->
            <v-tabs
              v-model="selectedSubTab"
              color="secondary"
              align-tabs="center"
              
            >
              <v-tab>Ingredients</v-tab>
              <v-tab>Nutrition</v-tab>
              <v-tab>Instructions</v-tab>
            </v-tabs>

            <!-- SUB TAB CONTENT -->
            <v-window v-model="selectedSubTab" class="mt-4">

              <!-- INGREDIENTS -->
              <v-window-item :value="0">
                <div style="display: flex; flex-direction: row; gap: 24px; align-items: flex-start; width: 100%;">

                  <!-- LEFT COLUMN: Ingredients + Budget + Image -->
                  <div style="flex: 1; min-width: 300px;">
                    <!-- Recipe Description -->
                    <p class="text-subtitle-1 mb-1" style="font-weight: 700; margin-top: 16px; color: #1976d2;">
                      Recipe Description:
                    </p>
                    <p class="text-body-1" style="margin-bottom: 16px">
                      {{ recipe.ingredientBlurb }}
                    </p>

                    <!-- Ingredients -->
                    <div class="d-flex flex-wrap ga-3 mt-2">
                      <v-chip
                        v-for="ingredient in recipe.ingredients"
                        :key="ingredient"
                        color="primary"
                        class="ingredient-chip"
                      >
                        {{ ingredient }}
                      </v-chip>
                    </div>

                    <!-- Budget Inputs -->
                    <v-card class="mt-4 pa-4" elevation="2" style="border-radius: 12px;">
                      <p class="text-subtitle-1 mb-2" style="font-weight: 700; color: #1976d2;">
                        Budget Preferences
                      </p>

                      <v-row>
                        <v-col cols="6">
                          <v-text-field
                            v-model="minBudget"
                            label="Min Budget ($)"
                            type="number"
                            variant="outlined"
                            density="comfortable"
                          />
                        </v-col>

                        <v-col cols="6">
                          <v-text-field
                            v-model="maxBudget"
                            label="Max Budget ($)"
                            type="number"
                            variant="outlined"
                            density="comfortable"
                          />
                        </v-col>
                      </v-row>

                      <v-btn
                        color="primary"
                        class="mt-2"
                        block
                        @click="getRecommendations"
                      >
                        Get Recommendations
                      </v-btn>
                    </v-card>

                    <!-- Image BELOW the budget -->
                    <v-img
                      :src="recipe.image"
                      height="350"
                      contain
                      style="border-radius: 12px; margin-top: 16px;"
                    />
                  </div>

                  <!-- RIGHT COLUMN: Recommendations -->
                  <div style="flex: 1; min-width: 300px;">
                    <h3 style="color:#1976d2; font-weight:700; margin-bottom: 8px;">
                      Store Recommendations
                    </h3>

                    <div v-if="!recommendations.length" style="font-size: 1em; color: #555;">
                      Enter budget preferences to get started.
                    </div>

                    <div v-else>
                      <v-list dense>
                        <v-list-item
                          v-for="(rec, index) in recommendations"
                          :key="index"
                          style="border-bottom: 1px solid #eee;"
                        >
                          <div>
                            <p style="margin:0;">
                              <strong>#{{ index + 1 }}:</strong>
                              Total Price: ${{ rec.total_price.toFixed(2) }},
                              Stores: {{ rec.num_stores }}
                            </p>
                            <p style="margin:0; font-size: 0.9em; color:#555;">
                              Stores: {{ Array.isArray(rec.stores) ? rec.stores.join(', ') : rec.stores || 'N/A' }}
                            </p>
                          </div>
                        </v-list-item>
                      </v-list>
                    </div>
                  </div>

                </div>
              </v-window-item>

              <!-- NUTRITION -->
               <v-window-item :value="1" class="pa-4">

                <v-row>

                  <!-- LEFT COLUMN: Pie Chart -->
                  <v-col cols="12" md="6">

                    <!-- 📘 Top-left explanation -->
                    <p class="text-body-1">
                      This chart shows how calories are distributed between protein, carbs, and fat.
                      Each section represents the percentage of total calories from each macronutrient.
                      It is listed in kcals/grams.
                    </p>

                    <!-- Pie Chart -->
                    <div class="d-flex justify-center mt-4">
                      <NutritionChart
                        :protein="recipe.nutrition.protein"
                        :carbs="recipe.nutrition.carbs"
                        :fat="recipe.nutrition.fat"
                        :calories="recipe.nutrition.calories"
                      />
                    </div>

                    <!-- Sodium -->
                    <p class="text-center mt-4">
                      <strong>Sodium:</strong> {{ recipe.nutrition.sodium }} mg
                    </p>

                  </v-col>

                  <!-- RIGHT COLUMN: Nutrition Score) -->
                  <v-col cols="12" md="6">
                    <div>
                      <!-- Example placeholder -->
                      <p class="text-body-1">Nutrition score blurb goes here and score goes below</p>
                    </div>

                  </v-col>

                </v-row>

              </v-window-item>

              <!-- INSTRUCTIONS -->
              <v-window-item :value="2">
                <div v-for="(section, sIndex) in recipes[selectedTab].instructions" :key="section.section || sIndex">
                  <!-- Optional section title -->
                  <h3 v-if="section.section" style="margin-top: 16px; color:#000000;">
                    {{ section.section }}
                  </h3>

                  <ol class="recipe-checklist" style="max-width: 600px; margin: 0;">
                    <li v-for="(step, stepIndex) in section.steps" :key="step">
                      <label style="cursor: pointer; display: flex; align-items: center;">
                        <input
                          type="checkbox"
                          v-model="checkedSteps[sIndex][stepIndex]"
                          style="margin-right: 12px;"
                        />
                        <span style="font-weight: 700; margin-right: 6px; color: #1976d2;">
                          {{ stepIndex + 1 }}.
                        </span>
                        <span :style="{ textDecoration: checkedSteps[sIndex][stepIndex] ? 'line-through' : 'none', color: '#333' }">
                          {{ step }}
                        </span>
                      </label>
                    </li>
                  </ol>
                </div>
              </v-window-item>

          </v-window>

        </v-card>

      </v-window-item>

    </v-window>

  </v-container>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import NutritionChart from '@/components/NutritionChart.vue'

const selectedTab = ref(0)
const selectedSubTab = ref(0)
const minBudget = ref<number | null>(null)
const maxBudget = ref<number | null>(null)
const recommendations = ref<any[]>([])
const recipes = [
  {
    name: "Baked Feta Pasta",
    id: 1,
    image: "https://helloyummy.co/wp-content/uploads/2021/02/baked-feta-pasta-recipe12.jpg",
    ingredients: ["8 Oz Baby Spinach", "1 Cup Cherry Tomatoes", "8 Oz Pasta (Any)", "2 Tbsp Olive Oil", "1 Feta Cheese Block", "Salt",  "Pepper",  "1 Tbsp Minced Garlic"],
    ingredientBlurb: "A creamy baked pasta dish where feta and tomatoes roast together to create a rich sauce.",
    nutrition: {calories: "382", protein: 7.5, carbs: 46.47, fat: 9.9, sodium: 318.11 },
    instructions: [
    {section: "Sauce",
      steps: [
        "Preheat oven to 400 degrees",
        "Place feta block in the middle of a oven safe pan",
        "Add spinach and cherry tomatoes to pan",
        "Drizzle pan with olive oil and minced garlic",
        "Season with salt and pepper",
        "Place in oven and cook for 25 minutes or until tomatoes have softened"]},
    {section: "Pasta (While sauce is cooking)",
      steps: [
        "Bring a large pot of salted water to a boil",      "Cook pasta as instructed on box",
        "Drain pasta with collander and set until when done"]},
    {section: "Assembly",
      steps: [
        "Once sauce is removed from the oven, stir everything until combined",
        "Toss in the pasta the sauce until it is fully dressed",
        "Enjoy!"]}
  ]},
  {
    name: "Overnight Oats",
    id: 2,
    image: "https://vegangirlsguide.com/wp-content/uploads/2024/09/overnight-oats-recipe-1725865416.jpg",
    ingredients: ["1/2 Cup Rolled Oats", "1/2 Cup Greek YOgurt", "1/2 Cup Milk", "Salt", "1 Tsp Chia Seeds", "2 Tsp Honey", "1/4 Cup Berries"],
    ingredientBlurb: "An easy make-ahead breakfast that sits overnight in the fridge.",
    nutrition: {calories: "352", protein: 7.5, carbs: 46.47, fat: 9.9, sodium: 318.11 },
    instructions: [
    {section: "Assembly",
      steps: [
        "Combine oats, yogurt, milk, salt, and chia seeds in a jar and stir well",
        "Refrigerate for 8-10 hours",
        "Top with fresh berries and honey",
        "Enjoy!"]},
  ]},
  {
    name: "Quesidilla",
    id: 3,
    image: "https://iheartvegetables.com/wp-content/uploads/2022/10/Mediterranean-Veggie-Sandwich-3-of-5.jpg",
    ingredients: ["enter here"],
    ingredientBlurb: "Blurb",
    nutrition: {calories: "352", protein: 7.5, carbs: 46.47, fat: 9.9, sodium: 318.11 },
    instructions: [
    {section: "Filling",
      steps: [
        "Season chicken breast with salt and pepper",
        "Heat a pan over medium heat and add olive oil",
        "Cook chicken breast for 5–7 minutes per side until fully cooked",
        "Remove chicken from pan and let rest for a few minutes",
        "Slice or shred the chicken into small pieces",
        "Rinse and drain black beans",
        "Add black beans to the pan and cook for 2–3 minutes until warmed"]},

    {section: "Tortilla (While filling is cooking)",
      steps: [
        "Heat a separate pan or skillet over medium heat",
        "Lightly butter one side of a large tortilla",
        "Place tortilla in the pan, buttered side down",
        "Sprinkle shredded cheddar cheese evenly over half of the tortilla"]},

    {section: "Assembly",
      steps: [
        "Add cooked chicken and black beans on top of the cheese",
        "Fold the tortilla in half over the filling",
        "Cook for 2–3 minutes until bottom is golden brown",
        "Flip and cook the other side until cheese is melted",
        "Remove from pan, slice into wedges, and enjoy!"]}
  ]},
   {
    name: "Taco Soup",
    id: 4,
    image: "https://iheartvegetables.com/wp-content/uploads/2022/10/Mediterranean-Veggie-Sandwich-3-of-5.jpg",
    ingredients: ["enter here"],
    ingredientBlurb: "Blurb",
    nutrition: {calories: "352", protein: 7.5, carbs: 46.47, fat: 9.9, sodium: 318.11 },
    instructions: [
    {section: "Base",
      steps: [
        "Heat a large pot over medium heat",
        "Add ground beef and cook until browned, breaking it up as it cooks",
        "Drain excess grease if needed",
        "Add diced onion and cook for 3–5 minutes until softened",
        "Season with salt and pepper"]},

    {section: "Soup (Build the flavor)",
      steps: [
        "Stir in taco seasoning and mix well",
        "Add diced tomatoes (with juices)",
        "Add kidney beans (drained and rinsed)",
        "Add sweet corn (drained)",
        "Stir everything together and bring to a simmer",
        "Reduce heat and let cook for 10–15 minutes, stirring occasionally"]},

    {section: "Assembly",
      steps: [
        "Ladle soup into bowls",
        "Top with shredded cheddar cheese",
        "Add sour cream on top",
        "Sprinkle Fritos for crunch",
        "Enjoy!"]}
  ]},
   {
    name: "Pancakes",
    id: 5,
    image: "https://iheartvegetables.com/wp-content/uploads/2022/10/Mediterranean-Veggie-Sandwich-3-of-5.jpg",
    ingredients: ["enter here"],
    ingredientBlurb: "Blurb",
    nutrition: {calories: "352", protein: 7.5, carbs: 46.47, fat: 9.9, sodium: 318.11 },
    instructions: [
    {section: "Dry Ingredients",
      steps: [
        "In a large bowl, combine whole wheat flour, white sugar, baking powder, baking soda, and salt",
        "Whisk together until evenly mixed"]},

    {section: "Wet Ingredients",
      steps: [
        "In a separate bowl, whisk together buttermilk, eggs, and vegetable oil until smooth"]},

    {section: "Batter & Cooking",
      steps: [
        "Pour wet ingredients into the dry ingredients and stir until just combined (do not overmix)",
        "Heat a pan or griddle over medium heat and lightly grease if needed",
        "Pour batter onto the pan to form pancakes",
        "Cook until bubbles form on the surface and edges look set (about 2–3 minutes)",
        "Flip and cook the other side until golden brown",
        "Remove from pan and repeat with remaining batter",
        "Serve warm and enjoy!"]}
  ]},
   {
    name: "Chicken Caesar Salad",
    id: 6,
    image: "https://iheartvegetables.com/wp-content/uploads/2022/10/Mediterranean-Veggie-Sandwich-3-of-5.jpg",
    ingredients: ["enter here"],
    ingredientBlurb: "Blurb",
    nutrition: {calories: "352", protein: 7.5, carbs: 46.47, fat: 9.9, sodium: 318.11 },
    instructions: [
    {section: "Chicken",
      steps: [
        "Season chicken breast with salt and pepper",
        "Heat a pan over medium heat and add a small amount of oil",
        "Cook chicken for 5–7 minutes per side until fully cooked",
        "Remove from heat and let rest for a few minutes",
        "Slice chicken into strips"]},

    {section: "Salad Base",
      steps: [
        "Wash and chop romaine lettuce into bite-sized pieces",
        "Place lettuce in a large bowl",
        "Add croutons and shredded parmesan cheese"]},

    {section: "Assembly",
      steps: [
        "Add sliced chicken on top of the salad",
        "Drizzle Caesar dressing over everything",
        "Toss until evenly coated",
        "Serve and enjoy!"]}
  ]},
   {
    name: "Unstuffed Peppers",
    id: 7,
    image: "https://iheartvegetables.com/wp-content/uploads/2022/10/Mediterranean-Veggie-Sandwich-3-of-5.jpg",
    ingredients: ["enter here"],
    ingredientBlurb: "Blurb",
    nutrition: {calories: "352", protein: 7.5, carbs: 46.47, fat: 9.9, sodium: 318.11 },
    instructions: [
    {section: "Rice",
      steps: [
        "Cook white rice according to package instructions",
        "Set aside once fully cooked"]},

    {section: "Base",
      steps: [
        "Heat a large pot or deep pan over medium heat",
        "Add olive oil",
        "Add diced white onion and cook for 3–5 minutes until softened",
        "Add minced garlic and cook for 1 minute until fragrant",
        "Add ground beef and cook until browned, breaking it up as it cooks",
        "Drain excess grease if needed",
        "Season with salt, paprika, oregano, and red pepper flakes"]},

    {section: "Peppers & Sauce",
      steps: [
        "Chop bell peppers into bite-sized pieces",
        "Add bell peppers to the pot and cook for 4–5 minutes until slightly softened",
        "Stir in crushed tomatoes",
        "Add beef broth and mix well",
        "Bring to a simmer and cook for 10–15 minutes, stirring occasionally"]},

    {section: "Assembly",
      steps: [
        "Stir in cooked rice until evenly combined",
        "Taste and adjust seasoning if needed",
        "Serve hot and enjoy!"]}
  ]},
   {
    name: "Meatloaf",
    id: 8,
    image: "https://iheartvegetables.com/wp-content/uploads/2022/10/Mediterranean-Veggie-Sandwich-3-of-5.jpg",
    ingredients: ["enter here"],
    ingredientBlurb: "Blurb",
    nutrition: {calories: "352", protein: 7.5, carbs: 46.47, fat: 9.9, sodium: 318.11 },
    instructions: [
    {section: "Prep",
      steps: [
        "Preheat oven to 375 degrees",
        "Dice white onion into small pieces",
        "Lightly grease a loaf pan or baking dish with olive oil"]},

    {section: "Meat Mixture",
      steps: [
        "In a large bowl, combine ground beef, diced onion, Italian bread crumbs, egg, and milk",
        "Season with salt",
        "Mix everything together until just combined (do not overmix)"]},

    {section: "Assembly & Baking",
      steps: [
        "Transfer the mixture into the prepared pan and shape into a loaf",
        "Place in the oven and bake for 45–55 minutes or until fully cooked",
        "Remove from oven and let rest for 5–10 minutes before slicing",
        "Serve and enjoy!"]}
  ]},
  {
    name: "Beef & Avocado Burrito",
    id: 9,
    image: "https://iheartvegetables.com/wp-content/uploads/2022/10/Mediterranean-Veggie-Sandwich-3-of-5.jpg",
    ingredients: ["enter here"],
    ingredientBlurb: "Blurb",
    nutrition: {calories: "352", protein: 7.5, carbs: 46.47, fat: 9.9, sodium: 318.11 },
    instructions: [
    {section: "Rice",
      steps: [
        "Cook white rice according to package instructions",
        "Set aside once fully cooked"]},

    {section: "Filling",
      steps: [
        "Heat a pan over medium heat and add olive oil",
        "Add ground beef and cook until browned, breaking it up as it cooks",
        "Season with salt (and pepper if desired)",
        "In a separate pan, cook egg to preference (scrambled or fried)",
        "Slice avocado into thin pieces"]},

    {section: "Assembly",
      steps: [
        "Warm tortilla in a pan or microwave until soft",
        "Add a layer of rice to the center of the tortilla",
        "Top with cooked ground beef",
        "Add egg, avocado slices, and shredded Mexican style cheese",
        "Fold in the sides and roll into a burrito",
        "Serve and enjoy!"]}
  ]},
  {
    name: "Veggie Sandwich",
    id: 10,
    image: "https://iheartvegetables.com/wp-content/uploads/2022/10/Mediterranean-Veggie-Sandwich-3-of-5.jpg",
    ingredients: ["enter here"],
    ingredientBlurb: "Blurb",
    nutrition: {calories: "352", protein: 7.5, carbs: 46.47, fat: 9.9, sodium: 318.11 },
    instructions: [
    {section: "Prep",
      steps: [
        "Slice tomato, cucumber, red onion, and avocado",
        "Wash and dry lettuce and sprouts",
        "Lightly season tomato and avocado with salt"]},

    {section: "Bread",
      steps: [
        "Spread mayonnaise on one slice of sourdough bread",
        "Spread Dijon mustard on the other slice",
        "Add cheese of choice to one side"]},

    {section: "Assembly",
      steps: [
        "Layer lettuce, tomato, cucumber, red onion, avocado, and sprouts onto the bread",
        "Close the sandwich with the other slice of bread",
        "Slice in half and serve"]}
  ]}
]

// Interactive checklist state
const checkedSteps = ref(recipes[0].instructions.map(() => false))

// Reset checklist when switching recipes
watch(selectedTab, (newVal) => {
  checkedSteps.value = recipes[newVal].instructions.map(() => false)
  recommendations.value = []
})

const getRecommendations = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        recipe_id: recipes[selectedTab.value].id,
        min_budget: minBudget.value,
        max_budget: maxBudget.value,
        sort_by: null,
        filters: null
      })
    })

    const data = await response.json()
    recommendations.value = data.recommendations.slice(0, 10)
    console.log("Backend response:", recommendations.value)

  } catch (error) {
    console.error("Error fetching recommendations:", error)
  }
}
</script>

<style scoped>
.main-title {
  font-weight: 800;
  margin-top: 15px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}
.psu-logo {
  height: 40px;
  width: auto;
}
.bold-title {
  font-weight: 800;
  font-size: 28px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

/* Checklist styling */
.recipe-checklist {
  padding-left: 0;
  list-style: none;
  margin-top: 12px;
}

.recipe-checklist li {
  margin-bottom: 12px;
  line-height: 1.5;
  font-size: 16px;
}

/* Ingredient chip hover effect */
.ingredient-chip {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  cursor: pointer;
}

.ingredient-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
</style>