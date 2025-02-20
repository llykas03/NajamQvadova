import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/HomeView.vue';
import Login from '../components/Login.vue';
import NewUser from '@/components/NewUser.vue';
import Client from '../views/ClientView.vue';
import AdminKorisnici from '@/views/adminKorisnici.vue';
import AdminVozila from '@/views/adminVozila.vue';
import AdminNewUser from '@/components/AdminNewUser.vue';
import KorisnikIzmena from '@/components/KorisnikIzmena.vue';
import VoziloIzmena from '@/components/VoziloIzmena.vue';
import AdminNewViacle from '@/components/AdminNewViacle.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dodaj-vozilo',
    name: 'Dodaj-Vozilo',
    component: AdminNewViacle
  },
  {
    path: '/new-user-admin',
    name: 'New-user-admin',
    component: AdminNewUser
  },
  {
    path: '/new-user',
    name: 'New-user',
    component: NewUser
  },
  {
    path: '/korisnik-izmena',
    name: 'korisnik-izmena',
    meta: { requiresRole: ["administrator"] },
    component: KorisnikIzmena
  },
  {
    path: '/vozilo-izmena',
    name: 'vozilo-izmena',
    meta: { requiresRole: ["administrator"] },
    component: VoziloIzmena
  },
  {
    path: '/client',
    name: 'Client',
    component: Client,
    meta: { requiresRole: ["administrator", "user"] },
  },
  {
    path: '/admin-korisnici',
    name: 'Admin-korisnici',
    component: AdminKorisnici,
    meta: { requiresRole: ["administrator"] },
  },
  {
    path: '/admin-vozila',
    name: 'AdminVozila',
    component: AdminVozila,
    meta: { requiresRole: ["administrator"] },
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Middleware za zaštitu ruta
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('user'); // Proveravamo da li postoji korisnik u localStorage

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); // Ako nije prijavljen, preusmeri ga na login stranicu
  } else {
    next(); // Inače, pusti ga da nastavi dalje
  }
});

export default router;
