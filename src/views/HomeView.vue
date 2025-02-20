<template>
  <div id="app">
    <div class="container">
      <div class="left-a-side">
        <h2>Mesto gde se snovi ostvaruju</h2>
        <p>Nikad niste vozili kvad ili bagi? A imatge zelju, na pravom ste mestu! Kod nas imate veliki izbor ovakvih terenskih vozila. Nase je najam i odrzavanje, vase da voizte gde god pozelte!</p>
        
        <!-- Dugme za preusmeravanje na login stranicu -->
        <button class="hero-btn" @click="$router.push('/login')">Prijavi se</button>
      </div>
      
      <div class="right-a-side">
        <div class="img">
          <img src="../assets/img/Hero-section-img.png" alt="Hero Image">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue';

export default {
  name: 'HomeView',
  components: {
    Navbar
  }
};
</script>

<style>
.container {
  display: flex;
  height: 100vh;
  justify-content: center;
  align-items: center;
}
#app {
  background-image: url('../assets/img/Home-Hero.png');
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
}
p, h2 {
  color: white;
  padding: 10px 0;
}
.hero-btn {
  padding: 10px 20px;
  background-color: wheat;
  color: black;
}
</style>
