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

                <!-- blurb -->
                <p class="text-body-1 text-center">
                  {{ recipe.ingredientBlurb }}
                </p>
                
                <!-- horizontal ingredients -->
                <div class="d-flex flex-wrap ga-3 mt-2">

                  <v-chip
                    v-for="ingredient in recipe.ingredients"
                    :key="ingredient"
                    color="primary"
                  >
                    {{ ingredient }}
                  </v-chip>

                </div>

              </v-window-item>

              <!-- NUTRITION -->
               <v-window-item :value="1">

                <p><strong>Calories:</strong> {{ recipe.nutrition.calories }}</p>

                <div class="d-flex justify-left mt-4">
                  <NutritionChart
                    :protein="recipe.nutrition.protein"
                    :carbs="recipe.nutrition.carbs"
                    :fat="recipe.nutrition.fat",
                    :sodium="recipe.nutrition.sodium"
                  />
                </div>

              </v-window-item>

              <!-- INSTRUCTIONS -->
              <v-window-item :value="2">

              <div v-for="section in recipe.instructions" :key="section.section" class="mb-6">

                <!-- Section Title -->
                <h3 class="text-subtitle-1 font-weight-bold mb-2 text-center">
                  {{ section.section }}
                </h3>

                <!-- Steps -->
                <ol class="text-left" style="max-width: 600px; margin: 0 auto;">
                  <li
                    v-for="step in section.steps"
                    :key="step"
                    class="mb-1"
                  >
                    {{ step }}
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



<!-- ALL INFO INPUTTED BELOW -->
<script setup lang="ts">
import { ref } from 'vue'
import NutritionChart from '@/components/NutritionChart.vue'

const selectedTab = ref(0)
const selectedSubTab = ref(0)

const recipes = [

{
  name: "Baked Feta Pasta",

  ingredients: [
    "8 Oz Baby Spinach",
    "1 Cup Cherry Tomatoes",
    "8 Oz Pasta (Any)",
    "2 Tbsp Olive Oil",
    "1 Feta Cheese Block",
    "Salt",
    "Pepper",
    "1 Tbsp Minced Garlic"
  ],

  ingredientBlurb:
    "A creamy baked pasta dish where feta and tomatoes roast together to create a rich sauce. Serves 4.",

  nutrition: {
  calories: "520",
  protein: 18,
  carbs: 60,
  fat: 20,
  sodium: 20
 },

  instructions: [
  {
    section: "Sauce",
    steps: [
      "Preheat oven to 400 degrees",
      "Place feta block in the middle of a oven safe pan",
      "Add spinach and cherry tomatoes to pan",
      "Drizzle pan with olive oil and minced garlic",
      "Season with salt and pepper",
      "Place in oven and cook for 25 minutes or until tomatoes have softened"
    ]
  },
  {
    section: "Pasta (While sauce is cooking)",
    steps: [
      "Bring a large pot of salted water to a boil",
      "Cook pasta as instructed on box",
      "Drain pasta with collander and set until when done"
    ]
  },
  {
    section: "Assembly",
    steps: [
      "Once sauce is removed from the oven, stir everything until combined",
      "Toss in the pasta the sauce until it is fully dressed",
      "Enjoy!"
    ]
  }
]
},

{
  name: "Overnight Oats",

  ingredients: [
    "Oats",
    "Milk",
    "Chia seeds",
    "Honey"
  ],

  ingredientBlurb:
    "An easy make-ahead breakfast that sits overnight in the fridge.",

  nutrition: {
  calories: "520",
  protein: 18,
  carbs: 60,
  fat: 20,
  sodium: 20
 },

  instructions: [
    "Mix ingredients",
    "Refrigerate overnight",
    "Eat cold in the morning"
  ]
}

]
</script>

<style scoped>
.main-title {
  font-weight: 800;
  margin-top: 15px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;       /* vertically align logo and text */
  justify-content: center;   /* center the container horizontally */
  gap: 12px;                 /* space between logo and title */
}
.psu-logo {
  height: 40px;  /* adjust as needed */
  width: auto;   /* maintain aspect ratio */
}

</style>
