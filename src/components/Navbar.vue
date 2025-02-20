<script setup>
import { RouterLink, useRoute, useRouter } from "vue-router";
import { toast } from "vue3-toastify";
import { ref, onMounted, watchEffect } from "vue";

// Vue Router instance
const router = useRouter();
const route = useRoute();

// Reaktivna promenljiva za korisničku rolu i login status
const userRole = ref(null);
const isLoggedIn = ref(false);

// Funkcija za dobijanje korisničke uloge i provera tokena
const checkUserRole = () => {
  userRole.value = localStorage.getItem("rola") || "korisnik"; // Default: "korisnik"
  isLoggedIn.value = !!localStorage.getItem("access_token"); // Provera da li postoji token
};

// Automatski prati promene u localStorage i osvežava navbar
watchEffect(() => {
  checkUserRole();
});

// Funkcija za logout
const handleLogout = async () => {
  try {
    localStorage.removeItem("access_token");
    localStorage.removeItem("rola");

    // Osvežavanje navbar-a nakon logout-a
    checkUserRole();

    toast.success("Uspešno ste se odjavili.");
    router.push("/login");
  } catch (error) {
    toast.error(error.message || "Greška pri odjavi.");
  }
};

// Funkcija za proveru aktivne rute
const isActiveLink = (path) => {
  return route.path === path;
};
</script>

<template>
  <nav class="navbar">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/"> SajtoQvad </RouterLink>

      <div class="navbar-links">
        <RouterLink class="nav-link" to="/" :class="{ active: isActiveLink('/') }">
          Početna
        </RouterLink>
        <RouterLink
          v-if="isLoggedIn"
          class="nav-link"
          to="/client"
          :class="{ active: isActiveLink('/client') }"
        >
          Pretplata
        </RouterLink>
        <RouterLink
          v-if="isLoggedIn && userRole === 'administrator'"
          class="nav-link"
          to="/admin-korisnici"
          :class="{ active: isActiveLink('/admin-korisnici') }"
        >
          Korisnici
        </RouterLink>
        <RouterLink
          v-if="isLoggedIn && userRole === 'administrator'"
          class="nav-link"
          to="/admin-vozila"
          :class="{ active: isActiveLink('/admin-vozila') }"
        >
          Vozila
        </RouterLink>
      </div>

      <!-- Dugme za odjavu, prikazuje se samo ako korisnik ima token -->
      <button v-if="isLoggedIn" class="logout-btn" @click="handleLogout">
        <i class="fas fa-sign-out-alt"></i> Logout
      </button>
    </div>
  </nav>
</template>

<style scoped>
/* Glavni stilovi za navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #3C3D37;
  padding: 10px 20px;
}

/* Stilizacija linkova */
.navbar-links {
  display: flex;
  gap: 15px;
}

.nav-link {
  color: #ECDFCC;
  text-decoration: none;
  padding: 8px 15px;
  background-color: #697565;
  border-radius: 5px;
  transition: 0.3s;
}

.nav-link:hover {
  background-color: #5a6b52;
}

/* Stil aktivnog linka */
.nav-link.active {
  font-weight: bold;
  background-color: #4d5d42;
}

/* Logout dugme */
.logout-btn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.3s;
}

.logout-btn:hover {
  background-color: #cc0000;
}
</style>
