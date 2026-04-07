<template>
  <v-app>
    <!-- App Bar -->
    <v-app-bar app color="primary" dark elevation="4" height="80">
      <v-container fluid class="d-flex align-center">
        
        <!-- Sidebar Toggle -->
        <v-app-bar-nav-icon 
          v-if="route.params.slug" 
          @click="sidebarVisible = true"
        />

        <v-spacer />

        <! Help Button>
        <v-btn  class="mr-4" color="secondary" variant="elevated" @click="helpDialog = true">
          Introduction
        </v-btn>

        <v-dialog v-model="helpDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h6">
              How to Use This Website
            </v-card-title>

            <v-card-text>
              <ul>
                <li>Welcome to Penn State Nutrition App! This app will help you shop, cook, and learn all about your nutrition. It is made for Penn State students by Penn State students! </li>
                <li>Below you can scroll through 10 unique recipes. On each recipe there are 3 tabs that will help you</li>
                <li>Ingredients: The left side listsa ll of the ingredients you will need. On the right side, input your desired budget and number of stoes you want to go to, and it will output your shopping list. </li>
                <li>Nutrition:  The left side will give you your overall nutritional value. The right side will give you a calculated nutrition score  </li>
                <li>Instructions: This will will give you step by step instructions to make the recipe. </li>
              </ul>
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn color="primary" @click="helpDialog = false">
                Got it
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>


      </v-container>
    </v-app-bar>
    
    <!-- Navigation Drawer -->
    <v-navigation-drawer 
      v-model="sidebarVisible" 
      temporary
      class="app-sidebar"
    >
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main class="main-content">

      <!-- Router View -->
      <router-view />

      <!-- Footer -->
      <Footer />
    </v-main>

    <!-- Snackbar -->
  
  </v-app>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Footer from '@/components/Footer.vue'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

const route = useRoute()
const router = useRouter()

const sidebarVisible = ref(false)

const showBreadcrumbs = computed(() => {
  return route.name !== 'Home'
})

const breadcrumbItems = computed(() => {
  const items = [
    { title: 'Home', to: '/' }
  ]

  if (route.params.slug) {
    items.push({
      title: route.params.slug as string,
      to: `/${route.params.slug}`
    })
  }

  return items
})

const navigateToCatalog = () => {
  if (!route.params.slug) return
  router.push(`/catalog/${route.params.slug}`)
  sidebarVisible.value = false
}

const navigateToDetails = () => {
  if (!route.params.slug) return
  router.push(`/inventory/${route.params.slug}/details`)
  sidebarVisible.value = false
}

const navigateToReports = () => {
  if (!route.params.slug) return
  router.push(`/inventory/${route.params.slug}/report`)
  sidebarVisible.value = false
}

const helpDialog = ref(false)

</script>


   


<style lang="scss" scoped>
.brand-logo {
  text-decoration: none;
  color: inherit;
  
  .logo-img {
    height: 50px;
    width: auto;
  }
  
  .brand-text {
    .brand-title {
      font-size: 1.5rem;
      font-weight: 600;
      line-height: 1.2;
    }
    
    .brand-subtitle {
      font-size: 0.875rem;
      opacity: 0.9;
      line-height: 1;
    }
  }
}

.user-info {
  .user-name {
    font-size: 0.95rem;
    font-weight: 500;
    line-height: 1.2;
  }
  
  .user-role {
    font-size: 0.8rem;
    opacity: 0.8;
    line-height: 1;
  }
}

.user-btn {
  border-radius: 8px !important;
  font-weight: 500 !important;
}

.user-menu {
  min-width: 200px;

  .gap-1 {
    gap: 0.25rem;
  }

  .flex-1 {
    flex: 1;
  }

  .shell-status-text {
    font-size: 0.75rem;
    opacity: 0.7;
    line-height: 1.3;
  }
}

.main-content {
  background: #eceeff;
  min-height: calc(100vh - 80px);
}

.app-sidebar {
  :deep(.v-navigation-drawer) {
    background: #1976d2;
    color: white;
    width: 300px;
  }
  
  .sidebar-header {
    text-align: center;
    padding: 2rem 1rem;
    background: rgba(0, 0, 0, 0.1);
    
    .sidebar-logo {
      max-width: 250px;
      height: auto;
    }
  }
  
  .sidebar-item {
    color: white;
    text-align: center;
    margin: 1rem 0;
    font-size: 1.2rem;
    
    &:hover {
      background: rgba(255, 255, 255, 0.1);
    }
  }
  
  .sidebar-footer {
    text-align: center;
    padding: 2rem;
    background: rgba(0, 0, 0, 0.1);
    
    .thon-logo {
      max-height: 75px;
      max-width: 150px;
    }
  }
}

.breadcrumbs-section {
  background: rgba(30, 30, 30, 0.95);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.75rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  
  :deep(.v-breadcrumbs-item) {
    color: rgba(255, 255, 255, 0.7);
  }
  
  :deep(.v-breadcrumbs-item--link) {
    color: white;
  }
  
  :deep(.v-breadcrumbs-divider) {
    color: rgba(255, 255, 255, 0.5);
  }
}

.no-access-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 999;
}

// Responsive adjustments
@media (max-width: 960px) {
  .brand-text {
    display: none;
  }
  
  .logo-img {
    height: 40px !important;
  }
  
  .user-info {
    display: none;
  }
}
</style>

