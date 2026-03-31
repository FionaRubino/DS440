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

          <div v-if="loading[index]">
            <p>Loading...</p>
          </div>

          <div v-else>
            <div v-if="recommendations[index] && recommendations[index].length">
              <div v-for="(combo, i) in recommendations[index]" :key="i">
                <p>
                  Total: {{ combo.total_price }} | Stores: {{ combo.num_stores }}
                </p>

                <div v-for="(store, ingredient) in combo.stores" :key="ingredient">
                  {{ ingredient }} → {{ store }}
                </div>

                <hr />
              </div>
            </div>
            <div v-else>
              <p>No recommendations available for this recipe/budget.</p>
            </div>
          </div>

        </v-card>
      </v-window-item>
    </v-window>

  </v-container>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'

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

// store results per tab
const recommendations = ref<{ [key: number]: any[] }>({})
const loading = ref<{ [key: number]: boolean }>({})

// fetch function
const fetchRecommendations = async (index: number) => {
  loading.value[index] = true
  try {
    const res = await axios.post("http://127.0.0.1:5000/api/recommend", {
      recipe_id: index + 1,  // make sure CSV recipe IDs match
      min_budget: 0,        // adjust budget as needed
      max_budget: 100
    })
    recommendations.value[index] = res.data.recommendations
  } catch (err) {
    console.error("Error fetching recommendations:", err)
    recommendations.value[index] = []
  } finally {
    loading.value[index] = false
  }
}

// run when tab changes
watch(selectedTab, (newIndex) => {
  if (!recommendations.value[newIndex]) {
    fetchRecommendations(newIndex)
  }
})

// initial fetch for first tab
fetchRecommendations(0)
</script>