<template>
  <v-container class="fill-height d-flex flex-column align-center justify-center">
    
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
        <v-card width="400" class="pa-4 text-center">
          <h2>{{ recipe }}</h2>
          <p>Here you can add details for {{ recipe }}.</p>
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

const selectedTab = ref(0)
</script>
