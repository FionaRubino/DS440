<template>
  <v-app>
    <v-container
      fluid
      class="d-flex justify-center pt-12"
      style="min-height: 100vh;"
    >
      <div style="width: 100%; max-width: 1400px; text-align: center;">

        <!-- App Title -->
        <h1 class="mb-8">State College Nutrition Tracker</h1>

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
                  <h2 style="padding-bottom: 32px;">{{ recipe }}</h2>
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
