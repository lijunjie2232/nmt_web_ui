import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import 'vuetify/styles'

const vuetify = createVuetify({
    ssr: true,
    icons: {
        defaultSet: 'mdi', // This is already the default value - only for display purposes
    },
})
