<script setup lang="ts">
import { ref, watch, nextTick } from "vue"
import Chart from "chart.js/auto"
import ChartDataLabels from "chartjs-plugin-datalabels"

Chart.register(ChartDataLabels)

const props = defineProps({
  protein: Number,
  carbs: Number,
  fat: Number,
  calories: Number
})

const chartRef = ref<HTMLCanvasElement | null>(null)
let chartInstance: Chart | null = null

watch(
  [() => props.protein, () => props.carbs, () => props.fat, () => props.calories],
  async () => {
    await nextTick()
    if (!chartRef.value) return

    if (chartInstance) chartInstance.destroy()

    // 👉 Convert grams to calories
    const proteinCal = (props.protein || 0) * 4
    const carbsCal = (props.carbs || 0) * 4
    const fatCal = (props.fat || 0) * 9

    chartInstance = new Chart(chartRef.value, {
      type: "doughnut",
      data: {
        labels: ["Protein", "Carbs", "Fat"],
        datasets: [
          {
            data: [proteinCal, carbsCal, fatCal],
            backgroundColor: ["#42A5F5", "#66BB6A", "#FFA726"],
            borderWidth: 0
          }
        ]
      },
      options: {
        cutout: "50%", // 👈 makes it a doughnut
        responsive: true,
        plugins: {
          legend: { position: "bottom" },

          // ✅ Labels on slices (percent)
          datalabels: {
            color: "#fff",
            font: { weight: "bold" },
            formatter: (value, ctx) => {
              const total = ctx.chart.data.datasets[0].data.reduce((a: number, b: number) => a + b, 0)
              const percent = ((value / total) * 100).toFixed(0)
              return percent + "%"
            }
          }
        }
      },
      plugins: [
  {
          id: "centerText",
          beforeDraw(chart) {
            const { ctx, chartArea } = chart
            if (!chartArea) return

            const centerX = (chartArea.left + chartArea.right) / 2
            const centerY = (chartArea.top + chartArea.bottom) / 2

            ctx.save()

            // 👇 smaller, cleaner font
            ctx.font = "900 16px sans-serif"
            ctx.fillStyle = "#333"
            ctx.textAlign = "center"
            ctx.textBaseline = "middle"

            ctx.fillText(`${props.calories} kcal`, centerX, centerY)

            ctx.restore()
          }
        }
      ]
    })
  },
  { immediate: true }
)
</script>

<template>
  <div style="width: 300px; height: 300px;">
    <canvas ref="chartRef"></canvas>
  </div>
</template>