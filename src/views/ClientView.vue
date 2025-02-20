<template>
  <div id="client-home">
    <div class="container-client">
      <div v-for="atv in atvs" :key="atv.id" class="card">
        <img :src="atv.urlSlika" :alt="atv.name" class="atv-image">
        <h3>{{ atv.ime }}</h3>
        <p>{{ atv.konjskeSnage }} KS | {{ atv.kubikaza }} cc | {{ atv.gorivo }}</p>
        <div class="status">
          <span>{{ atv.cenaRadnogSata }}$/h</span>
          <span :class="['status-indicator', atv.statusVozila === 'Slobodno' ? 'green' : 'red']"></span>
        </div>
        <button 
          class="use-btn" 
          @click="showUserModal(atv.id)" 
          :disabled="atv.statusVozila !== 'Slobodno'"
        >
          Use
        </button>
      </div>
    </div>

    <div class="modal-overlay" :style="{ display: modalDisplay }">
      <div class="modal">
        <h2>Informacije o kvadu</h2>
        <div v-if="selectedAtv">
          <img :src="selectedAtv.urlSlika" :alt="selectedAtv.ime" class="atv-image">
          <h3>{{ selectedAtv.ime }}</h3>
          <p>{{ selectedAtv.konjskeSnage }} KS | {{ selectedAtv.kubikaza }} cc | {{ selectedAtv.gorivo }}</p>
          <p><strong>Cena radnog sata:</strong> {{ selectedAtv.cenaRadnogSata }}$/h</p>
          <p><strong>Status:</strong> {{ selectedAtv.statusVozila }}</p>
        </div>

        <h2>Informacije o korisniku</h2>
        <div v-if="userInfo">
          <p><strong>Ime:</strong> {{ userInfo.ime }}</p>
          <p><strong>Prezime:</strong> {{ userInfo.prezime }}</p>
          <p><strong>Kredit:</strong> {{ userInfo.kredit }}$</p>
          <p><strong>Email:</strong> {{ userInfo.email }}</p>
        </div>

        <div class="rental-section">
          <label for="rentalHours">Broj sati:</label>
          <input type="number" id="rentalHours" v-model="rentalHours" min="1" />
          <p><strong>Ukupna cena:</strong> {{ totalPrice }}$</p>
          <button @click="rentAtv" class="rent-btn">Iznajmi</button>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        </div>

        <button @click="closeModal" class="close-btn">Zatvori</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ipAdress } from '@/main';
import { onMounted } from 'vue';

export default {
  name: 'ClientHome',
  data() {
    return {
      atvs: [],
      modalDisplay: 'none',
      selectedAtv: null,
      userInfo: null,
      rentalHours: 1,
      errorMessage: "",
    };
  },
  computed: {
    totalPrice() {
      return this.selectedAtv ? this.selectedAtv.cenaRadnogSata * this.rentalHours : 0;
    }
  },
  mounted() { // Koristimo mounted umesto created
    this.fetchAtvs();
  },
  methods: {
    async fetchAtvs() {
      try {
        const response = await axios.get(ipAdress +'/vozilaa');
        console.log(response.data);
        this.atvs = response.data;
      } catch (error) {
        console.error('Došlo je do greške pri dobijanju podataka:', error);
      }
    },
    async showUserModal(atvId) {
      this.selectedAtv = this.atvs.find(atv => atv.id === atvId);
      const loggedInUser = localStorage.getItem("id");

      if (loggedInUser) {
        try {
          const response = await axios.get(ipAdress +`/GETkorisnik/${loggedInUser}`);
          console.log(response.data);
          this.userInfo = response.data;
          this.modalDisplay = 'block';
        } catch (error) {
          console.error('Greška pri dobijanju korisničkih podataka:', error);
        }
      } else {
        console.error('Nema podataka o ulogovanom korisniku.');
      }
    },
    async rentAtv() {
      this.errorMessage = "";

      if (!this.selectedAtv || !this.userInfo) {
        this.errorMessage = "Greška: Nema podataka o kvadu ili korisniku.";
        return;
      }

      const ukupnaCena = this.selectedAtv.cenaRadnogSata * this.rentalHours;

      if (this.userInfo.kredit >= ukupnaCena) {
        try {
          const loggedInUser = localStorage.getItem("id");
          const response = await axios.post(ipAdress + '/dodaj_rezervaciju', {
            idVozila: this.selectedAtv.id,
            idKorisnika: loggedInUser,
            satnica: this.rentalHours.toString()
          });

          console.log("Uspešno iznajmljeno:", response.data);
          alert("Uspešno ste iznajmili kvad!");

          this.closeModal();
          window.location.reload(); // Refresh nakon uspješnog iznajmljivanja
        } catch (error) {
          console.error("Greška prilikom iznajmljivanja:", error);
          this.errorMessage = "Došlo je do greške pri iznajmljivanju.";
        }
      } else {
        this.errorMessage = "Nemate dovoljno kredita za iznajmljivanje.";
      }
    },
    closeModal() {
      this.modalDisplay = 'none';
      this.selectedAtv = null;
      this.userInfo = null;
      this.rentalHours = 1;
      this.errorMessage = "";
    }
  }
};
</script>

<style scoped>
 #app {
    overflow: unset;
  }
  /* Stilovi za kartice i ostale elemente */
  #client-home {
    background-color: #E6D6BE;
    min-height: 100vh;
    padding: 20px;
  }
  
  .container-client {
    display: flex;
    justify-content: space-evenly;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .card {
    background-color: #1D2D13;
    padding: 15px;
    border-radius: 10px;
    width: 300px;
  }
  
  .atv-image {
    width: 100%;
    height: auto;
    border-radius: 5px;
  }
  
  h3 {
    color: white;
    margin: 10px 0;
  }
  
  .status {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 10px 0;
    color: white;
  }
  
  .status-indicator {
    width: 20px;
    height: 20px;
    border-radius: 50%;
  }
  
  .green {
    background-color: #31B131;
  }
  
  .red {
    background-color: red;
  }
  
  .use-btn {
    background-color: black;
    color: white;
    padding: 5px 10px;
    border: none;
    cursor: pointer;
    width: 100%;
  }
  
  .use-btn:hover {
    background-color: gray;
  }
  
  /* Stilovi za modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  p, h2 {
    color: white;
  }
  .modal {
    background-color: #1D2D13;
    padding: 20px;
    border-radius: 10px;
    max-width: 400px;
    max-height: 600px;
    width: 100%;
    text-align: center;
    display: block;
    position: relative;
  }
  
  .user-avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin-bottom: 10px;
  }
  
  .close-btn {
    background-color: #ff4d4d;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  .close-btn:hover {
    background-color: #cc0000;
  }
/* Sekcija za unos sati i dugme za iznajmljivanje */
.rental-section {
  margin-top: 15px;
}

#rentalHours {
  width: 100%;
  padding: 5px;
  font-size: 16px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.rent-btn {
  background-color: #28a745;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-top: 10px;
}

.rent-btn:hover {
  background-color: #218838;
}

.error-message {
  color: red;
  font-weight: bold;
  margin-top: 5px;
}

/* Stilovi za modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background-color: #1D2D13;
  padding: 20px;
  border-radius: 10px;
  max-width: 400px;
  max-height: 600px;
  width: 100%;
  text-align: center;
  display: block;
  position: relative;
}

.close-btn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

.close-btn:hover {
  background-color: #cc0000;
}
</style>
