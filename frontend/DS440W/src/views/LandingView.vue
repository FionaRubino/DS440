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

          <h2 class="text-center bold-title">{{ recipe.name }}</h2>

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
              <div class="d-flex flex-wrap align-start ga-6">

                <!-- LEFT SIDE: text + ingredients -->
                <div style="flex: 1; min-width: 250px;">

                  <p class="text-subtitle-1 mb-1" style="font-weight: 700; margin-top: 16px; color: #1976d2;">
                    Recipe Description:
                  </p>
                  <p class="text-body-1" style = "margin-bottom: 16px">
                    {{ recipe.ingredientBlurb }}
                  </p>

                  <!-- ingredients -->
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

                </div>

                <!-- RIGHT SIDE: image -->
                <div style="flex: 1; min-width: 250px;">
                  <v-img
                    :src="recipe.image"
                    height="350"
                    contain
                    style="border-radius: 12px;"
                  />
                </div>

              </div>
            </v-window-item>

            <!-- NUTRITION -->
            <v-window-item :value="1">
              <p><strong>Calories:</strong> {{ recipe.nutrition.calories }}</p>

              <div class="d-flex justify-center mt-4">
                <NutritionChart
                  :protein="recipe.nutrition.protein"
                  :carbs="recipe.nutrition.carbs"
                  :fat="recipe.nutrition.fat"
                />
              </div>
            </v-window-item>

            <!-- INSTRUCTIONS -->
            <v-window-item :value="2">
              <ol class="recipe-checklist">
                <li v-for="(step, index) in recipe.instructions" :key="step">
                  <label style="cursor: pointer; display: flex; align-items: center;">
                    <!-- Checkbox first -->
                    <input type="checkbox" v-model="checkedSteps[index]" style="margin-right: 12px;" />
                    <!-- Step number manually -->
                    <span style="font-weight: 700; margin-right: 6px; color: #1976d2;">{{ index + 1 }}.</span>
                    <span :style="{ textDecoration: checkedSteps[index] ? 'line-through' : 'none', color: '#333' }">
                      {{ step }}
                    </span>
                  </label>
                </li>
              </ol>
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

const recipes = [
  {
    name: "Baked Feta Pasta",
    image: "https://helloyummy.co/wp-content/uploads/2021/02/baked-feta-pasta-recipe12.jpg",
    ingredients: ["Feta cheese","Cherry tomatoes","Olive oil","Garlic","Pasta"],
    ingredientBlurb: "A creamy baked pasta dish where feta and tomatoes roast together to create a rich sauce.",
    nutrition: { calories: "520", protein: 18, carbs: 60, fat: 20 },
    instructions: [
      "Preheat the oven to 400°F (200°C).",
      "Bring a large pot of salted water to a boil. Cook the linguine according to package directions until al dente. Drain and set aside.",
      "In a large Dutch oven or any oven-safe dish, add the salmon fillets, olive oil, Boursin cheese, spinach, cherry tomatoes, garlic, capers, Italian seasoning, salt, and pepper.",
      "Cover the dish with a lid or foil and bake for 20–30 minutes, or until the salmon flakes easily with a fork and the tomatoes have softened.",
      "Remove the dish from the oven and gently flake the salmon into bite-sized pieces. Stir everything together until the cheese is melted and well combined into a creamy sauce.",
      "Add the cooked linguine and toss until fully coated in the Boursin sauce. Serve hot with fresh herbs or a squeeze of lemon, if desired."
    ]
  },
  {
    name: "Overnight Oats",
    image: "https://vegangirlsguide.com/wp-content/uploads/2024/09/overnight-oats-recipe-1725865416.jpg",
    ingredients: ["Oats","Milk","Chia seeds","Honey"],
    ingredientBlurb: "An easy make-ahead breakfast that sits overnight in the fridge.",
    nutrition: { calories: "520", protein: 18, carbs: 60, fat: 20 },
    instructions: ["Mix ingredients","Refrigerate overnight","Eat cold in the morning"]
  },
  {
    name: "Veggie Sandwich",
    image: "https://iheartvegetables.com/wp-content/uploads/2022/10/Mediterranean-Veggie-Sandwich-3-of-5.jpg",
    ingredients: ["enter here"],
    ingredientBlurb: "Blurb",
    nutrition: { calories: "520", protein: 18, carbs: 60, fat: 20 },
    instructions: ["Blurb"]
  }
]

// Interactive checklist state
const checkedSteps = ref(recipes[0].instructions.map(() => false))

// Reset checklist when switching recipes
watch(selectedTab, (newVal) => {
  checkedSteps.value = recipes[newVal].instructions.map(() => false)
})
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