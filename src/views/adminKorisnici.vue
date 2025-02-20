<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useRouter, RouterLink } from "vue-router";
import TableContainer from "@/components/TableContainer.vue";
import { ipAdress } from "@/main";

const korisnici = ref([]);
const korisnikToDelete = ref(null);
const router = useRouter();
const confirmModalRef = ref(null);

const fetchKorisnici = async () => {
  try {
    const response = await axios.get(ipAdress +"/admin-korisnici");
    korisnici.value = response.data;
    // korisnici.value = korisnici._rawValue
  } catch (error) {
    toast.error(error.response?.data?.message || error.message);
  }
};

const handleIzmena = (korisnik) => {
  localStorage.setItem('izmenaID', korisnik);
  router.push(`/korisnik-izmena`);
};

const handleDelete = (korisnik) => {
  korisnikToDelete.value = korisnik;
  deleteKorisnik();
};

const deleteKorisnik = async () => {
  try {
    const response = await axios.post(ipAdress + `/admin-k-brisanje/${korisnikToDelete.value.id}`);
    korisnici.value = korisnici.value.filter(
      (korisnik) => korisnik.id !== korisnikToDelete.value.id
    );
    korisnikToDelete.value = null;
    confirmModalRef.value.hideModal();
  } catch (error) {
    console.log(error.response?.data?.message || error.message);
  }
};

onMounted(() => {
  fetchKorisnici();
});
</script>

<template>
  <TableContainer to="/new-user-admin" buttonText="Dodaj korisnika">
    <template #table-header>
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Ime</th>
        <th scope="col">Prezime</th>
        <th scope="col">Srednje ime</th>
        <th scope="col">JMBG</th>
        <th scope="col">Broj licne karte</th>
        <th scope="col">Email</th>
        <th scope="col">ID kvada</th>
        <th scope="col">Kredit</th>
        <th scope="col">Rola</th>
        <th scope="col">Akcije</th>
      </tr>
    </template>
    <template #table-body>
      <tr v-for="korisnik in korisnici" :key="korisnik.id">
        <td>{{ korisnik.id }}</td>
        <td>{{ korisnik.ime }}</td>
        <td>{{ korisnik.prezime }}</td>
        <td>{{ korisnik.srednje_ime }}</td>
        <td>{{ korisnik.jmbg }}</td>
        <td>{{ korisnik.broj_licne_karte }}</td>
        <td>{{ korisnik.email }}</td>
        <td>{{ korisnik.trenutniKorisnik }}</td>
        <td>{{ korisnik.kredit }}</td>
        <td>{{ korisnik.rola }}</td>
        <td>
          <button
            @click="handleIzmena(korisnik.id)"
            class="text-warning mx-1 btn btn-link"
          >
            <i class="fas fa-edit"></i>
          </button>
          <button
            @click="handleDelete(korisnik)"
            class="text-danger mx-1 btn btn-link"
          >
            <i class="fas fa-trash"></i>
          </button>
        </td>
      </tr>
    </template>
  </TableContainer>
</template>