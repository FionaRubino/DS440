<template>
  <footer class="app-footer">
    <v-container>
      <v-row class="py-6">
        <v-col cols="12" md="3" class="text-center text-md-left">
        </v-col>
        
        <!-- Links Sections -->
        <v-col cols="6" md="3">
          <h6 class="footer-title mb-3">Connect</h6>
          <div class="social-buttons mb-4">
            <v-btn 
              icon
              size="small"
              href="https://www.facebook.com/" 
              target="_blank"
              class="social-btn facebook"
            >
              <v-icon>mdi-facebook</v-icon>
            </v-btn>
            <v-btn 
              icon
              size="small"
              href="https://www.youtube.com/"
              target="_blank"
              class="social-btn youtube"
            >
              <v-icon>mdi-youtube</v-icon>
            </v-btn>
            <v-btn 
              icon
              size="small"
              href="https://www.instagram.com" 
              target="_blank"
              class="social-btn instagram"
            >
              <v-icon>mdi-instagram</v-icon>
            </v-btn>
          </div>
        </v-col>
      </v-row>
      
      <!-- Bottom Section -->
      <v-divider class="mb-4" />
    </v-container>

  </footer>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
</script>

<style lang="scss" scoped>
.app-footer {
 background: rgb(var(--v-theme-primary));
  color:white;
  margin-top: auto;
  
  .footer-logo {
    max-width: 150px;
    height: auto;
    opacity: 0.9;
  }

  .footer-title {
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: rgb(var(--v-theme-secondary));
    font-size: 0.875rem;
  }
  
  .footer-links {
    display: flex;
    flex-direction: column;
    gap: 8px;
    
    .footer-link {
      color: rgba(255, 255, 255, 0.8);
      text-decoration: none;
      font-size: 0.875rem;
      line-height: 1.4;
      transition: color 0.2s ease;
      
      &:hover {
        color: rgb(var(--v-theme-secondary));
        text-decoration: none;
      }
    }
  }
  
  .social-buttons {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    
    .social-btn {
      color: white;
      transition: all 0.3s ease;
      
      &.facebook {
        &:hover {
          background-color: #1877f2;
          color: white;
        }
      }
      
      &.twitter {
        &:hover {
          background-color: #1da1f2;
          color: white;
        }
      }
      
      &.youtube {
        &:hover {
          background-color: #ff0000;
          color: white;
        }
      }
      
      &.instagram {
        &:hover {
          background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%);
          color: white;
        }
      }
      
      &:hover {
        transform: translateY(-2px);
      }
    }
  }
  
  .footer-bottom {
    padding: 1rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 1rem;
  }
}

/* Instant overlay, no fade */
.center-logo {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(10, 10, 10, 0.8);
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  cursor: pointer;
}

.sidebar-logo-popup {
  width: 220px;
  height: auto;
}

// Responsive adjustments
@media (max-width: 960px) {
  .app-footer {
    .footer-logo {
      max-width: 120px;
    }
    
    .social-buttons {
      justify-content: center;
      margin-bottom: 1rem;
    }
  }
}

@media (max-width: 600px) {
  .app-footer {
    .footer-title {
      font-size: 0.8rem;
      margin-bottom: 0.75rem !important;
    }
    
    .footer-links .footer-link {
      font-size: 0.8rem;
    }
    
    .social-buttons {
      gap: 6px;
      
      .social-btn {
        min-width: 36px !important;
        width: 36px !important;
        height: 36px !important;
      }
    }
  }
}
</style>