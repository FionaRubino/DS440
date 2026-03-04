<template>
  <v-container fluid class="fill-height d-flex flex-column">
    
    
    <h1 class="mb-8">Welcome to Your Recipe App!</h1>

    <!-- Tabs -->
    <v-tabs v-model="selectedTab" color="primary">
      <v-tab v-for="(recipe, index) in recipes" :key="index">
        {{ recipe }}
      </v-tab>
    </v-tabs>

    <!-- Content -->
    <v-window v-model="selectedTab" class="mt-6">
      <v-window-item v-for="(recipe, index) in recipes" :key="index">
        <v-card class="pa-4 text-center">
          <h2>{{ recipe }}</h2>
          <p>Here you can add details for {{ recipe }}.</p>
          
           <!-- SUB TABS -->
          <v-tabs
            v-model="selectedSubTab"
            color="secondary"
            align-tabs="center"
          >
            <v-tab v-for="tab in subTabs" :key="tab">
              {{ tab }}
            </v-tab>
          </v-tabs>

          <!-- SUB TAB CONTENT -->
          <v-window v-model="selectedSubTab" class="mt-4">
            <v-window-item
              v-for="tab in subTabs"
              :key="tab"
            >
              <div class="text-center pa-4">
                <h3>{{ tab }}</h3>
                <p>
                  Content for <strong>{{ recipe }}</strong> - {{ tab }}
                </p>
              </div>
            </v-window-item>
          </v-window>


        </v-card>
      </v-window-item>
    </v-window>

  </v-container>
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

const subTabs = ["Ingredients", "Nutrition", "Instruction"]

const selectedTab = ref(0)
const selectedSubTab = ref(0)
</script>
