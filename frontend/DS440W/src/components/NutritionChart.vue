<template>
  <div style="width: 300px; height: 300px;">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from "vue"
import Chart from "chart.js/auto"

const props = defineProps({
  protein: Number,
  carbs: Number,
  fat: Number,
  sodium: Number
})

const chartRef = ref<HTMLCanvasElement | null>(null)
let chartInstance: Chart | null = null

// Redraw chart whenever props change or component becomes visible
watch(
  [() => props.protein, () => props.carbs, () => props.fat, () => props.sodium, ],
  async () => {
    await nextTick()
    if (!chartRef.value) return

    // Destroy previous chart before creating a new one
    if (chartInstance) chartInstance.destroy()

    chartInstance = new Chart(chartRef.value, {
      type: "pie",
      data: {
        labels: ["Protein", "Carbs", "Fat", "Sodium"],
        datasets: [
          {
            data: [
              props.protein || 0,
              props.carbs || 0,
              props.fat || 0,
              props.sodium || 0
            ],
            backgroundColor: ["#42A5F5", "#66BB6A", "#FFA726", "#FF3856"]
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: "bottom" } }
      }
    })
  },
  { immediate: true }
)
</script><h1></h1>