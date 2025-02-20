<template>
    <div class="login-page">
      <div class="login-container">
        <div class="login-box">
          <h2 class="logo-text">SajtoQvad Logo</h2>
          <form @submit.prevent="createVehicle">
            <label>Ime</label>
            <input type="text" v-model="ime" required />
  
            <label>Boja</label>
            <input type="text" v-model="boja" required />
  
            <label>Registracija</label>
            <input type="text" v-model="registracija" required />
  
            <label>Gorivo</label>
            <input type="text" v-model="gorivo" required />
  
            <label>Motor</label>
            <input type="text" v-model="motor" required />
  
            <label>Kubikaža</label>
            <input type="number" v-model="kubikaza" required />
  
            <label>Konjske snage</label>
            <input type="number" v-model="konjskeSnage" required />
  
            <label>Status vozila</label>
            <select v-model="statusVozila">
              <option value="Slobodno">Slobodno</option>
              <option value="Zauzeto">Zauzeto</option>
            </select>
  
            <label>Godina proizvodnje</label>
            <input type="number" v-model="godinaProizvodnje" required />
  
            <label>Cena radnog sata</label>
            <input type="number" v-model="cenaRadnogSata" required />
  
            <button type="submit">Kreiraj vozilo</button>
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
        boja: "",
        registracija: "",
        gorivo: "",
        motor: "",
        kubikaza: 0,
        konjskeSnage: 0,
        statusVozila: "dostupno",
        godinaProizvodnje: 0,
        cena: 0,
        brojIznajmljivanja: 0,
        cenaRadnogSata: 0,
        radniSati: 0,
        errorMessage: ""
      };
    },
    methods: {
      async createVehicle() {
        try {
          const vehicleData = {
            ime: this.ime,
            boja: this.boja,
            registracija: this.registracija,
            gorivo: this.gorivo,
            motor: this.motor,
            kubikaza: this.kubikaza,
            konjskeSnage: this.konjskeSnage,
            statusVozila: this.statusVozila,
            godinaProizvodnje: this.godinaProizvodnje,
            cenaRadnogSata: this.cenaRadnogSata,
          };
  
          await axios.post(ipAdress + '/admin-vozilo-novo', vehicleData);
          alert("Vozilo uspešno kreirano!");
        } catch (error) {
          console.error("Došlo je do greške pri kreiranju vozila:", error);
          this.errorMessage = "Došlo je do greške pri kreiranju vozila. Pokušajte ponovo.";
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
  