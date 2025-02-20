// import { createStore } from 'vuex';

// export default createStore({
//   state: {
//     isLoggedIn: false,
//     userRole: null,
//   },
//   mutations: {
//     SET_USER_DATA(state, { role }) {
//       state.isLoggedIn = true;
//       state.userRole = role;
//     },
//     CLEAR_USER_DATA(state) {
//       state.isLoggedIn = false;
//       state.userRole = null;
//     },
//   },
//   actions: {
//     login({ commit }, { role }) {
//       commit('SET_USER_DATA', { role });
//       localStorage.setItem('rola', role); // Opcionalno: čuvaj i u localStorage
//     },
//     logout({ commit }) {
//       commit('CLEAR_USER_DATA');
//       localStorage.removeItem('rola'); // Opcionalno: briši iz localStorage
//     },
//   },
// });