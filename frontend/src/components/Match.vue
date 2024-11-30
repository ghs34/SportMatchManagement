<template>
  <div class="card">
    <h5 class="card-header">{{ id }}</h5>
    <div class="card-body">
      <img :src="imageUrl" class="card-img-top">
      <h5 class="card-title">Informació</h5>
      <p class="card-text"><strong>ID:</strong> {{id}}</p>
      <p class="card-text"><strong>Local:</strong> {{local_id}}</p>
      <p class="card-text"><strong>Visitor:</strong> {{visitor_id}}</p>
      <p class="card-text"><strong>Data:</strong> {{date}}</p>
      <p class="card-text"><strong>Price:</strong> {{price}}</p>
      <p class="card-text"><strong>Tickets:</strong> {{total_available_tickets}}</p>
      <p class="card-text"><strong>Competition:</strong> {{competition_id}}</p>
      <p class="card-text"><strong>logged:</strong> {{isLogged}}</p>
      <button @click="buyTicket" v-if=isLogged> Buy ticket </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Match',
  props: ['id', 'local_id', 'visitor_id', 'date', 'price', 'total_available_tickets', 'competition_id', 'quantity', 'imageUrl', 'isLogged'],
  methods: {
    buyTicket () {
      this.$emit('buyTicket', this.id)
    }
  }
}
</script>
