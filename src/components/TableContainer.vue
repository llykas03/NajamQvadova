<script setup>
import { defineProps } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  to: {
    type: String,
    required: true,
  },
  buttonText: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="my-5 justify-content-end">
        <RouterLink :to="to" role="button" class="btn btn-primary">
          {{ buttonText }}
        </RouterLink>
      </div>
      <div class="row">
        <table class="table">
          <thead class="thead-dark">
            <slot name="table-header"></slot>
          </thead>
          <tbody>
            <slot name="table-body"></slot>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
