import 'vuetify/styles'
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#001f54',
          secondary: '#9ccef7' // navy
        },
      },
    },
  },
})
