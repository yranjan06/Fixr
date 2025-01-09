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


// navigation guards
router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresLogin)){
        if (!store.state.loggedIn){
            next({path : '/login'})
        } else if (to.meta.role && to.meta.role != store.state.role){
            alert('role not authorized')
             next({path : '/'})
        } else {
            next();
        }
    } else {
        next();
    }
})


export default router;