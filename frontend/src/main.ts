import { createApp } from 'vue'
import { createPinia } from 'pinia'
import NaiveUI from 'naive-ui'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(NaiveUI)
app.use(router)

app.mount('#app')
