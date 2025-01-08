import HomePage from '../pages/HomePage.js'
import LoginPage from '../pages/LoginPage.js'
import CustomerRegisterPage from '../pages/CustomerRegisterPage.js'
import ProfessionalRegisterPage from '../pages/ProfessionalRegisterPage.js'

const routes = [
    { path: '/', component: HomePage },
    { path: '/login', component: LoginPage },
    { path: '/register/customer', component: CustomerRegisterPage },
    { path: '/register/professional', component: ProfessionalRegisterPage },
]

const router = new VueRouter({
    routes
})

export default router