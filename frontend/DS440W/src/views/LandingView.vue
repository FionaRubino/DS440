<template>
  <v-app>
    <v-container
      fluid
      class="d-flex justify-center pt-12"
      style="min-height: 100vh;"
    >
      <div style="width: 100%; max-width: 900px; text-align: center;">

        <h1 class="mb-8">State College Nutrition Tracker</h1>

        <!-- Centered Tabs -->
        <v-tabs
          v-model="selectedTab"
          color="primary"
          centered
        >
          <v-tab
            v-for="(recipe, index) in recipes"
            :key="index"
            :value="index"
          >
            {{ recipe }}
          </v-tab>
        </v-tabs>

        <!-- Arrow Buttons -->
        <v-row class="mt-2" justify="center" align="center">
          <v-btn
            icon
            class="ma-1"
            @click="selectedTab = Math.max(selectedTab - 1, 0)"
          >
            ◀
          </v-btn>
          <v-btn
            icon
            class="ma-1"
            @click="selectedTab = Math.min(selectedTab + 1, recipes.length - 1)"
          >
            ▶
          </v-btn>
        </v-row>

        <!-- Recipe Window -->
        <v-window v-model="selectedTab" class="mt-6">
          <v-window-item
            v-for="(recipe, index) in recipes"
            :key="index"
            :value="index"
          >
            <v-row justify="center">
              <v-col cols="12" sm="10" md="8" lg="8">

                <!-- TOP CARD -->
                <v-card class="mt-6 mb-4 pa-6 text-center">
                  <h2>{{ recipe }}</h2>
                  <p>Here you can add details for {{ recipe }}.</p>

                  <div class="d-flex justify-space-between mt-4">
                    <v-btn
                      color="primary"
                      @click="selectedSection = 'recipe'"
                    >
                      Recipe
                    </v-btn>

                    <v-btn
                      color="secondary"
                      @click="selectedSection = 'ingredients'"
                    >
                      Ingredients/Stores
                    </v-btn>

                    <v-btn
                      color="success"
                      @click="selectedSection = 'nutrition'"
                    >
                      Nutrition Info
                    </v-btn>
                  </div>
                </v-card>

                <!-- NEW BOTTOM CARD -->
                <v-card class="pa-6 text-center">

                  <div v-if="selectedSection === 'recipe'">
                    <h3>Recipe</h3>
                    <p>This is where the recipe instructions will go.</p>
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

const selectedTab = ref(0)

/* NEW STATE */
const selectedSection = ref('recipe')
</script>
