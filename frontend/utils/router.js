import Login from "../pages/Login.js";
import CustomerRegister from "../pages/CustomerRegister.js";
import ProviderRegister from "../pages/ProviderRegister.js";
import AdminDashboard from "../pages/AdminDashboard.js";
import CustomerDashboard from "../pages/CustomerDashboard.js";
import ProviderDashboard from "../pages/ProviderDashboard.js";

const Home = {
    template: `
        <div class="container mt-5">
            <h1>Welcome to Household Service App</h1>
            <p>Find reliable service providers for your household needs</p>
        </div>
    `
};

const routes = [
    { path: '/', component: Home },
    { path: '/login', component: Login },
    { path: '/register', component: CustomerRegister },
    { path: '/provider-register', component: ProviderRegister },
    { 
        path: '/admin-dashboard', 
        component: AdminDashboard, 
        meta: { requiresAuth: true, role: 'admin' }
    },
    { 
        path: '/customer-dashboard', 
        component: CustomerDashboard, 
        meta: { requiresAuth: true, role: 'customer' }
    },
    { 
        path: '/provider-dashboard', 
        component: ProviderDashboard, 
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