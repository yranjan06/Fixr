import LoginPage from "../pages/LoginPage.js";
import CustomerRegisterPage from "../pages/CustomerRegisterPage.js";
import ProviderRegisterPage from "../pages/ProviderRegisterPage.js";
import AdminDashboardPage from "../pages/AdminDashboardPage.js";
import CustomerDashboardPage from "../pages/CustomerDashboardPage.js";
import ProviderDashboardPage from "../pages/ProviderDashboardPage.js";

const HomePage = {
    template: `
        <div class="container mt-5">
            <h1>Welcome to Household Service App</h1>
            <p>Find reliable service providers for your household needs</p>
        </div>
    `
};

const routes = [
    { path: '/', component: HomePage },
    { path: '/login', component: LoginPage },
    { path: '/register', component: CustomerRegisterPage },
    { path: '/provider-register', component: ProviderRegisterPage },
    { 
        path: '/admin-dashboard', 
        component: AdminDashboardPage, 
        meta: { requiresAuth: true, role: 'admin' }
    },
    { 
        path: '/customer-dashboard', 
        component: CustomerDashboardPage, 
        meta: { requiresAuth: true, role: 'customer' }
    },
    { 
        path: '/provider-dashboard', 
        component: ProviderDashboardPage, 
        meta: { requiresAuth: true, role: 'provider' }
    }
];

const router = new VueRouter({
    routes
});

router.beforeEach((to, from, next) => {
    const store = router.app.$store;
    
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!store.state.loggedIn) {
            next('/login');
        } else if (to.meta.role && !store.state.userRoles.includes(to.meta.role)) {
            alert('Unauthorized access');
            next('/');
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;