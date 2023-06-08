import ProductDetails from './pages/ProductDetails/ProductDetails.svelte';
import QuerySearchPage from './pages/QuerySearch/QuerySearch.svelte';
import RegistredProductsPage from './pages/Products/Products.svelte';
import TrendsPage from './pages/Trends/Trends.svelte';
import LoginPage from './pages/Login/Login.svelte';
import UsersPage from './pages/Users/Users.svelte';
import ProductPositioning from './pages/ProductPositioning/ProductPositioning.svelte';
import ReportsPage from './pages/Reports/Reports.svelte';
import SystemEvents from './pages/SystemEvents/SystemEvents.svelte';
import TrackedProducts from './pages/TrackedProducts/TrackedProducts.svelte';

const routes = {
    '/': QuerySearchPage,
    '/registered-products': RegistredProductsPage,
    '/login': LoginPage,
    '/tracked-products': TrackedProducts,
    '/system-users': UsersPage,
    '/product-details': ProductDetails,
    '/trends/:meli_id': TrendsPage,
    '/positioning': ProductPositioning,
    '/system-reports': ReportsPage,
    '/system-events': SystemEvents
}

export { routes };