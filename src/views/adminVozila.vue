<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useRouter, RouterLink } from "vue-router";
import TableContainer from "@/components/TableContainer.vue";
import { ipAdress } from "@/main";

const vozila = ref([]); // promenjeno u vozila
const voziloToDelete = ref(null);
const router = useRouter();
const confirmModalRef = ref(null);

// Funkcija za dobijanje podataka o vozilima
const fetchVozila = async () => {
  try {
    const response = await axios.get(ipAdress + "/admin-vozila");
    vozila.value = response.data;
  } catch (error) {
    toast.error(error.response?.data?.message || error.message);
  }
};

// Funkcija za izmenu vozila
const handleIzmena = (vozilo) => {
  localStorage.setItem('izmenaIDVozilo', vozilo.id); // sačuvaj ID vozila za izmenu
  router.push(`/vozilo-izmena`); // preusmeravanje na stranicu za izmenu
};

// Funkcija za brisanje vozila
const handleDelete = (vozilo) => {
  voziloToDelete.value = vozilo;
  deleteVozilo();
};

// Funkcija koja briše vozilo sa servera
const deleteVozilo = async () => {
  try {
    const response = await axios.post(ipAdress + `/admin-vozila-brisanje/${voziloToDelete.value.id}`);
    vozila.value = vozila.value.filter((vozilo) => vozilo.id !== voziloToDelete.value.id);
    voziloToDelete.value = null;
    confirmModalRef.value.hideModal();
  } catch (error) {
    console.log(error.response?.data?.message || error.message);
  }
};

onMounted(() => {
  fetchVozila();
});
</script>

<template>
  <TableContainer to="/dodaj-vozilo" buttonText="Dodaj vozilo">
    <template #table-header>
      <tr>
        <th scope="col">Ime</th>
        <th scope="col">Boja</th>
        <th scope="col">Registracija</th>
        <th scope="col">Gorivo</th>
        <th scope="col">Motor</th>
        <th scope="col">Kubikaza</th>
        <th scope="col">Konjske Snage</th>
        <th scope="col">Status Vozila</th>
        <th scope="col">Godina Proizvodnje</th>
        <th scope="col">cena</th>
        <th scope="col">Broj iznajmljivanja</th>
        <th scope="col">Radni sati</th>
        <th scope="col">Akcije</th>
      </tr>
    </template>
    <template #table-body>
      <tr v-for="vozilo in vozila" :key="vozilo.id">
        <td>{{ vozilo.ime }}</td>
        <td>{{ vozilo.boja }}</td>
        <td>{{ vozilo.registracija }}</td>
        <td>{{ vozilo.gorivo }}</td>
        <td>{{ vozilo.motor }}</td>
        <td>{{ vozilo.kubikaza }}</td>
        <td>{{ vozilo.konjskeSnage }}</td>
        <td>{{ vozilo.statusVozila }}</td>
        <td>{{ vozilo.godinaProizvodnje }}</td>
        <td>{{ vozilo.cenaRadnogSata }}</td>
        <td>{{ vozilo.brojIznajmljivanja }}</td>
        <td>{{ vozilo.satnicaUkupna }}</td>
        <td>
          <button @click="handleIzmena(vozilo)" class="text-warning mx-1 btn btn-link">
            <i class="fas fa-edit"></i>
          </button>
          <button @click="handleDelete(vozilo)" class="text-danger mx-1 btn btn-link">
            <i class="fas fa-trash"></i>
          </button>
        </td>
      </tr>
    </template>
  </TableContainer>
</template>
