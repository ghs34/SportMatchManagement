<template>
  <div class="card">
    <h5 class="card-header">{{ id }}</h5>
    <div class="card-body">
    <h5 class="card-title">Informació</h5>
    <p class="card-text"><strong>ID:</strong> {{id}}</p>
    <p class="card-text"><strong>Name:</strong> {{name}}</p>
    <p class="card-text"><strong>Category:</strong> {{category}}</p>
    <p class="card-text"><strong>Sport:</strong> {{sport}}</p>
    <p class="card-text"><strong>Teams:</strong> {{teams}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Competition',
  props: ['id', 'name', 'category', 'sport', 'teams']
}
</script>
