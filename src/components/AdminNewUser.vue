<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-box">
        <h2 class="logo-text">SajtoQvad Logo</h2>
        <form @submit.prevent="createUser">
          <label>Ime</label>
          <input type="text" v-model="ime" required />

          <label>Srednje ime</label>
          <input type="text" v-model="srednjeIme" required />

          <label>Prezime</label>
          <input type="text" v-model="prezime" required />

          <label>Email</label>
          <input type="email" v-model="email" required />

          <label>Lozinka</label>
          <input type="password" v-model="lozinka" required />

          <label>JMBG</label>
          <input type="text" v-model="jmbg" required />

          <label>Broj lične karte</label>
          <input type="text" v-model="brojLicneKarte" required />

          <label>Kredit</label>
          <input type="number" v-model="kredit" required />

          <label>Rola</label>
          <select v-model="rola">
            <option value="administrator">Admin</option>
            <option value="user">Korisnik</option>
          </select>

          <button type="submit">Kreiraj</button>
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ipAdress } from "@/main";
import axios from "axios";

export default {
  data() {
    return {
      ime: "",
      srednjeIme: "",
      prezime: "",
      email: "",
      lozinka: "",
      jmbg: "",
      brojLicneKarte: "",
      kredit: 0,
      rola: "korisnik",
      errorMessage: ""
    };
  },
  methods: {
    async createUser() {
      console.log("Pokušavam da kreiram korisnika...");
      try {
        const userData = {
          ime: this.ime,
          srednje_ime: this.srednjeIme,
          prezime: this.prezime,
          email: this.email,
          lozinka: this.lozinka,
          jmbg: this.jmbg,
          broj_licne_karte: this.brojLicneKarte,
          kredit: this.kredit,
          rola: this.rola,
          status: 1
        };

        const response = await axios.post(ipAdress + '/korisnik-novii', userData);

        // if (response.status === 201) {
        //   this.$router.push({ name: "Client" });
        // }
      } catch (error) {
        console.error("Došlo je do greške pri kreiranju korisnika:", error);
        this.errorMessage = "Došlo je do greške pri kreiranju korisnika. Pokušajte ponovo.";
      }
    }
  }
};
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
  background: #151e00;
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
}

input,
select {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: none;
  border-radius: 5px;
  background-color: #ecdfcc;
}

button {
  margin: 15px 0;
  background: #ecdfcc;
  border: none;
  padding: 10px;
  width: 100%;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background: #bfa98c;
}
</style>
