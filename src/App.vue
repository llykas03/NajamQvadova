<template>
  <!--  -->
  <div id="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style>
/* html {
  overflow: hidden;
} */
.container {
  display: flex;
  min-height: 100vh;
  justify-content: center;
  align-items: center;
}
#app {
  background-image: url('../src/assets/img/qvad-blue.png');
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
  overflow: hidden;
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
<!-- /admin-vozila -->