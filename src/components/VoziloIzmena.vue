<template>
    <div class="edit-page">
      <div class="edit-container">
        <div class="edit-box">
          <h2 class="logo-text">Izmena Vozila</h2>
          <form @submit.prevent="updateVehicle">
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
  
            <label>Konjske Snage</label>
            <input type="number" v-model="konjskeSnage" required />
  
            <label>Status Vozila</label>
            <select v-model="statusVozila">
              <option value="Slobodno">Slobodno</option>
              <option value="Zauzeto">Zauzeto</option>
            </select>
  
            <label>Godina Proizvodnje</label>
            <input type="number" v-model="godinaProizvodnje" required />
  
            <label>Cena Radnog Sata</label>
            <input type="number" v-model="cenaRadnogSata" required />
  
  
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
        cenaRadnogSata: 0,
        errorMessage: ""
      };
    },
    async created() {
      await this.fetchVehicleData();
    },
    methods: {
      async fetchVehicleData() {
        try {
          const vehicleId = localStorage.getItem('izmenaIDVozilo');
          const response = await axios.get(`${ipAdress}/GETvozilo/${vehicleId}`);
          const vehicleData = response.data;
  
          this.ime = vehicleData.ime || "";
          this.boja = vehicleData.boja || "";
          this.registracija = vehicleData.registracija || "";
          this.gorivo = vehicleData.gorivo || "";
          this.motor = vehicleData.motor || "";
          this.kubikaza = vehicleData.kubikaza || 0;
          this.konjskeSnage = vehicleData.konjskeSnage || 0;
          this.statusVozila = vehicleData.statusVozila || "dostupno";
          this.godinaProizvodnje = vehicleData.godinaProizvodnje || 0;
          this.cenaRadnogSata = vehicleData.cenaRadnogSata || 0;
        } catch (error) {
          console.error("Greška pri dohvaćanju podataka vozila:", error);
          this.errorMessage = "Ne možemo učitati podatke o vozilu.";
        }
      },
      async updateVehicle() {
        try {
            const vehicleId = localStorage.getItem('izmenaIDVozilo');
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
          await axios.post(`${ipAdress}/admin-vozilo-izmena/${vehicleId}`, vehicleData);
          alert("Podaci o vozilu uspešno ažurirani!");
        } catch (error) {
          console.error("Greška pri ažuriranju vozila:", error);
          this.errorMessage = "Došlo je do greške pri ažuriranju podataka.";
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .edit-page {
    background: url("../assets/img/Home-Hero.png") no-repeat center center fixed;
    background-size: cover;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .edit-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-grow: 1;
  }
  
  .edit-box {
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
  