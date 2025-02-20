<template>
    <div class="login-page">
      <div class="login-container">
        <div class="login-box">
          <h2 class="logo-text">SajtoQvad Logo</h2>
          <form @submit.prevent="updateUser">
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
  
            <button type="submit">Sačuvaj izmene</button>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ipAdress } from "@/main";
  import axios from "axios";

  const url = window.location.href;
  const id = url.substring(url.lastIndexOf("/") + 1);
  console.log(id); // Ispisuje ID iz URL-a
  
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
        rola: "",
        errorMessage: "",
        loggedInUser: "1" // Primer ID-a, treba ga dinamički uzeti iz auth sistema
      };
    },
    async created() {
      await this.fetchUserData();
    },
    methods: {
      async fetchUserData() {
        try {
        const userId = localStorage.getItem('izmenaID');
          const response = await axios.get(`${ipAdress}/GETkorisnik/${userId}`);
          const userData = response.data;
  
          // Popunjavanje polja sa dobijenim podacima
          this.ime = userData.ime || "";
          this.srednjeIme = userData.srednje_ime || "";
          this.prezime = userData.prezime || "";
          this.email = userData.email || "";
          this.lozinka = userData.lozinka || "";
          this.jmbg = userData.jmbg || "";
          this.brojLicneKarte = userData.broj_licne_karte || "";
          this.kredit = userData.kredit || 0;
          this.rola = userData.rola || "korisnik";
        } catch (error) {
          console.error("Greška pri dohvaćanju podataka korisnika:", error);
          this.errorMessage = "Ne možemo učitati podatke o korisniku.";
        }
      },
      async updateUser() {
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
            rola: this.rola
          };
          const userId = localStorage.getItem('izmenaID');
          await axios.post(`${ipAdress}/admin-k-izmena/${userId}`, userData);
          alert("Podaci uspešno ažurirani!");
        } catch (error) {
          console.error("Greška pri ažuriranju korisnika:", error);
          this.errorMessage = "Došlo je do greške pri ažuriranju podataka.";
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
