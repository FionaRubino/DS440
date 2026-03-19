<template>
  <v-app>
    <v-container
      fluid
      class="d-flex justify-center pt-12"
      style="min-height: 100vh;"
    >
      <div style="width: 100%; max-width: 1400px; text-align: center;">

        <!-- App Title -->
        <div class="main-title">
          <img
            src="https://th.bing.com/th/id/OIP.1axdzj_b8TA5WMqnvJKx7gHaFj?w=256&h=192&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3"
            alt="PSU Logo"
            class="psu-logo"
          />
          <h1 class="main-title">State College Nutrition Tracker</h1>
        </div>

        <!-- Tabs with Side Arrows -->
        <div class="d-flex align-center justify-center mt-4" style="max-width: 900px; margin: auto; width: 100%;">
          <!-- Left Arrow -->
          <v-btn
            icon
            class="ma-2"
            @click="selectedTab = Math.max(selectedTab - 1, 0)"
          >
            ◀  
          </v-btn>

          <!-- Tabs -->
          <v-tabs
            v-model="selectedTab"
            color="primary"
            class="flex-grow-1"
            show-arrows
          >
            <v-tab
              v-for="(recipe, index) in recipes"
              :key="index"
              :value="index"
            >
              {{ recipe }}
            </v-tab>
          </v-tabs>

          <!-- Right Arrow -->
          <v-btn
            icon
            class="ma-2"
            @click="selectedTab = Math.min(selectedTab + 1, recipes.length - 1)"
          >
            ▶
          </v-btn>
        </div>

        <!-- Recipe Window -->
        <v-window v-model="selectedTab">
          <v-window-item
            v-for="(recipe, index) in recipes"
            :key="index"
            :value="index"
          >
            <v-row justify="center">

              <!-- TOP CARD (narrow, centered) -->
              <v-col cols="12" sm="10" md="8" lg="8">
                <v-card class="mt-6 mb-4 pa-6 text-center">
                  <h2 style="padding-bottom: 32px; font-weight: 800;">{{ recipe }}</h2>
                  <div class="d-flex justify-center mt-8" style="gap: 10px;">
                    <v-btn
                      :color="selectedSection === 'recipe' ? 'primary' : 'primary-lighten-2'"
                      @click="selectedSection = 'recipe'"
                    >
                      Recipe
                    </v-btn>

                    <v-btn
                      :color="selectedSection === 'ingredients' ? 'primary' : 'primary-lighten-2'"
                      @click="selectedSection = 'ingredients'"
                    >
                      Ingredients/Stores
                    </v-btn>

                    <v-btn
                      :color="selectedSection === 'nutrition' ? 'primary' : 'primary-lighten-2'"
                      @click="selectedSection = 'nutrition'"
                    >
                      Nutrition Info
                    </v-btn>
                  </div>
                </v-card>
              </v-col>

              <!-- BOTTOM CARD (wider than top card) -->
              <v-col cols="11" sm="11" md="11" lg="11">
                <v-card
                  class="mt-6 pa-12 text-center"
                  elevation="4"
                  style="margin: auto;"
                >
                  <div v-if="selectedSection === 'recipe'">
                    <h3 class="bold-title">Recipe</h3>

                    <!-- Flex container for steps left, image right -->
                    <div class="recipe-flex-reverse">
                      <!-- Numbered Steps -->
                      <ol class="steps-list">
                        <li v-for="(step, i) in recipeSteps[index]" :key="i">{{ step }}</li>
                      </ol>

                      <!-- Recipe Image -->
                      <v-img
                        :src="recipeImages[index]"
                        height="300"
                        cover
                        class="recipe-image rounded-lg"
                      ></v-img>
                    </div>
                  </div>

                  <div v-if="selectedSection === 'ingredients'">
                    <h3>Ingredients / Stores</h3>
                    <p>This section can list ingredients and where to buy them in State College.</p>
                  </div>

                  <div v-if="selectedSection === 'nutrition'">
                    <h3>Nutrition Info</h3>
                    <p>This section will contain calories, macros, and other nutrition facts.</p>
                  </div>
                </v-card>
              </v-col>

            </v-row>
          </v-window-item>
        </v-window>

      </div>
    </v-container>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const recipes = [
  "Baked Feta Pasta",
  "Overnight Oats",
  "Quesadilla",
  "Taco Soup",
  "Pancakes",
  "Chicken Caesar Salad",
  "Unstuffed Peppers",
  "Meatloaf",
  "Beef and Avocado Burrito",
  "Veggie Sandwich"
]

const recipeImages = [
  "https://helloyummy.co/wp-content/uploads/2021/02/baked-feta-pasta-recipe16-1.jpg",
  "https://source.unsplash.com/600x400/?overnight-oats",
  "https://source.unsplash.com/600x400/?quesadilla",
  "https://source.unsplash.com/600x400/?taco-soup",
  "https://source.unsplash.com/600x400/?pancakes",
  "https://source.unsplash.com/600x400/?caesar-salad",
  "https://source.unsplash.com/600x400/?stuffed-peppers",
  "https://source.unsplash.com/600x400/?meatloaf",
  "https://source.unsplash.com/600x400/?burrito",
  "https://source.unsplash.com/600x400/?veggie-sandwich"
]

const recipeSteps = [
  [
  "Mise En Place – Gather all your ingredients and get them prepped for a smooth cooking experience.",
  "Combine ingredients in a DUTCH OVEN – In a large Dutch oven or any oven-safe dish, add the salmon fillets, olive oil, Boursin cheese, spinach, cherry tomatoes, garlic, capers, Italian seasoning, salt, and pepper.",
  "Bake & Stir Together – Cover the dish with a lid or foil and bake for 20–30 minutes, or until the salmon flakes easily with a fork and the tomatoes have softened. Remove the dish from the oven and gently flake the salmon into bite-sized pieces. Stir everything together until the cheese is melted and well combined into a creamy sauce.",
  "Add Pasta & Stir Again – Add the cooked linguine and toss until fully coated in the Boursin sauce. Serve hot with fresh herbs or a squeeze of lemon, if desired.",
  "To Store – Let the pasta cool, then transfer it to an airtight container. Refrigerate for up to 3 days.",
  "To Reheat – Warm gently on the stovetop with a splash of milk or broth to loosen the sauce. You can also microwave it in 30-second bursts, stirring between each, until hot."
],
  ["Mix oats, milk, and yogurt", "Add fruits and nuts", "Refrigerate overnight", "Stir and enjoy in morning"],
  ["Place cheese and filling on tortilla", "Fold and cook on skillet", "Cut into pieces", "Serve with salsa"],
  ["Cook meat and beans", "Add spices and simmer", "Serve in bowls or tortillas"],
  ["Mix batter ingredients", "Heat skillet and pour batter", "Flip pancakes when bubbles form", "Serve with syrup"],
  ["Chop lettuce and chicken", "Mix with dressing", "Top with croutons and cheese"],
  ["Cook peppers and meat filling", "Combine in pan", "Bake for 25 minutes", "Serve warm"],
  ["Mix ground beef with spices", "Shape into loaf", "Bake for 1 hour", "Slice and serve"],
  ["Cook beef with seasonings", "Add avocado and veggies", "Wrap in tortilla", "Serve immediately"],
  ["Layer veggies on bread", "Add spread or dressing", "Top with another slice", "Cut and serve"]
]

const selectedTab = ref(0)
const selectedSection = ref('recipe')
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

.recipe-image {
  width: 100px;     /* fixed width for image */
  max-width: 35%;  /* responsive on smaller screens */
}
.bold-title {
  font-weight: 800; /* bold */
  margin-bottom: 20px;         /* remove extra spacing */
}
.v-tab {
  opacity: 0.7;
}
.v-card {
  transition: all 0.3s ease;
}
.v-card:hover {
  transform: translateY(-5px);
}

/* FLEX STYLING FOR RECIPE SECTION */
.recipe-flex-reverse {
  display: flex;
  justify-content: space-between; /* steps left, image right */
  align-items: flex-start;
  flex-wrap: wrap; /* responsive */
  width: 100%; /* take full width of card */
}

.steps-list {
  max-width: 500px; /* limits the width of the steps */
  text-align: left;
}
</style>