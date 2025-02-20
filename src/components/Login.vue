<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-box">
        <h2 class="logo-text">SajtoQvad Logo</h2>
        <form @submit.prevent="login">
          <label>Email</label>
          <input type="email" v-model="email" required />

          <label>Password</label>
          <input type="password" v-model="password" required />

          <button type="submit">Prijavi se</button>
        </form>
        <a class="new-user" @click="$router.push('/new-user')">Novi korisnik</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";
import { ipAdress } from "@/main.js";
import { onMounted } from 'vue';

const email = ref("");
const password = ref("");
const router = useRouter();

onMounted(() => {
  localStorage.clear();
});

async function login(props) {
  try {
    const response = await axios.post(ipAdress + "/login", {
      email: email.value,
      password: password.value,
    });

    localStorage.setItem("access_token", response.data.access_token);
    localStorage.setItem("id", response.data.id);
    localStorage.setItem("rola", response.data.rola);

    router.push("/client").then(() => console.log(response.data.message));
    
  } catch (error) {
    console.error("Došlo je do greške pri logovanju:", error);
    console.log("Došlo je do greške pri logovanju."); // Prikaži toast poruku o grešci
  }
}
</script>

  
  <style scoped>
  .login-page {
    background: url("../assets/img/Home-Hero.png") no-repeat center center fixed;
    background-size: cover;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-grow: 1;
  }
  
  .login-box {
    background: #151E00;
    padding: 40px;
    border-radius: 10px;
    text-align: center;
    color: white;
    width: 400px;
  }
  
  .logo-text {
    margin-bottom: 20px;
    font-size: 24px;
  }
  
  label {
    display: block;
    text-align: left;
    margin: 10px 0 5px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border: none;
    border-radius: 5px;
    background-color: #ECDFCC;
  }
  
  button {
    margin: 15px 0;
    background: #ECDFCC;
    border: none;
    padding: 10px;
    width: 100%;
    cursor: pointer;
    font-weight: bold;
  }
  
  button:hover {
    background: #bfa98c;
  }
  
  .new-user {
    text-decoration: none;
    color: #ECDFCC;
  }
  </style>
  