<template>
  <div class="app">
    <header class="header">
      <h1 class="title">Sport matches</h1>
      <div class="user-info" v-show="isLoggedIn">
        <span class="user-icon">👤</span>
        <span class="username">{{ username }}</span>
        <button class="balance" @click="showBalanceInput = !showBalanceInput">
          💰{{ balance.toFixed(2) }}€
        </button>
        <input
          v-show="showBalanceInput"
          type="number"
          v-model="balanceInput"
          @keyup.enter="addBalance"
          class="balance-input"
        />
      </div>
      <button class="close-basket" v-show="isLoggedIn" @click="toggleBasket">
        {{ basketVisible ? 'Tanca cistella' : 'Veure cistella' }}
        <span v-if="basketVisible" class="cart-count">{{ totalEntries }}</span>
      </button>
      <button class="login-btn" @click="login">{{ isLoggedIn ? 'Log Out' : 'Log In' }}</button>
    </header>

    <div class="container" v-show="basketVisible">
      <h2>Cart</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Sport</th>
            <th>Competition</th>
            <th>Match</th>
            <th>Quantity</th>
            <th>Price(&euro;)</th>
            <th>Total</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in data_matches" :key="index">
            <td>{{ item.sport }}</td>
            <td>{{ item.competition }}</td>
            <td>{{ item.local }} VS {{ item.visitor }}</td>
            <td>
              <div class="quantity-controls">
                <button class="decrement" @click="decrementQuantity(index)">-</button>
                {{ item.quantity }}
                <button class="increment" @click="incrementQuantity(index)">+</button>
              </div>
            </td>
            <td>{{ item.price }}</td>
            <td>{{ (item.quantity * item.price).toFixed(2) }}</td>
            <td>
              <button class="remove" @click="removeItem(index)">Eliminar entrada</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="actions">
        <button class="back" @click="toggleBasket">Enrere</button>
        <button class="finalize" @click="finalizePurchase">Finalitzar la compra</button>
      </div>
    </div>

    <div class="container" v-show="!basketVisible">
      <div class="match-card" v-for="(match, index) in catalog_matches" :key="index">
        <img :src="match.image" alt="Match Image" class="match-image"/>
        <div class="match-info">
          <h3>{{ match.sport }} - {{ match.level }}</h3>
          <p>{{ match.competition }}</p>
          <p>{{ match.teams }}</p>
          <p>{{ match.date }}</p>
          <p>{{ match.price }} €</p>
          <p>Entrades disponibles: {{ match.available }}</p>
          <button class="add-to-cart" v-show="isLoggedIn" @click="addToCart(match)">Afegeix a la cistella</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'Cart',
  data () {
    return {
      basketVisible: false,
      isLoggedIn: false,
      username: 'test',  // Nombre de usuario
      balance: 78.00,    // Cantidad de dinero
      balanceInput: 0,
      showBalanceInput: false,
      data_matches: [],
      data_competitions: [
        {
          id: 1,
          name: "Women's European Championship",
          sport: 'Volleyball'
        },
        {
          id: 2,
          name: '1st Division League',
          sport: 'Futsal'
        },
        {
          id: 3,
          name: '1st Division League',
          sport: 'Futsal'
        }
      ],
      catalog_matches: [
        {
          id: 1,
          sport: 'Volleyball',
          level: 'Senior',
          competition: "Women's European Championship",
          teams: 'Club Juventut Les Corts (Spain) vs CE Sabadell (Spain)',
          date: '2022-10-12',
          price: 4.3,
          available: 10,
          image: require('@/assets/volley.jpg')
        },
        {
          id: 2,
          sport: 'Futsal',
          level: 'Junior',
          competition: '1st Division League',
          teams: 'Club Juventut Les Corts (Spain) vs CE Sabadell (Spain)',
          date: '2022-07-10',
          price: 129.29,
          available: 690,
          image: require('@/assets/futsal.jpg')
        },
        {
          id: 3,
          sport: 'Futsal',
          level: 'Junior',
          competition: '1st Division League',
          teams: 'Club Juventut Les Corts (Spain) vs CE Sabadell (Spain)',
          date: '2022-08-10',
          price: 13.1,
          available: 990,
          image: require('@/assets/futsal.jpg')
        }
      ]
    }
  },
  computed: {
    totalEntries() {
      return this.data_matches.reduce((total, match) => total + match.quantity, 0);
    }
  },
  methods: {
    incrementQuantity (index) {
      this.data_matches[index].quantity++
    },
    decrementQuantity (index) {
      if (this.data_matches[index].quantity > 0) {
        this.data_matches[index].quantity--
      }
    },
    removeItem (index) {
      this.data_matches.splice(index, 1)
    },
    removeAllItems () {
      this.data_matches.splice(0, this.data_matches.length)
    },
    finalizePurchase () {
      let totalCost = 0;
      for (let match of this.data_matches) {
        const catalogMatch = this.catalog_matches.find(m => m.id === match.id);
        if (match.quantity > catalogMatch.available) {
          alert(`No puedes comprar más entradas de las disponibles para ${match.local} VS ${match.visitor}.`);
          return;
        }
        totalCost += match.quantity * match.price;
      }
      if (totalCost > this.balance) {
        alert('No tienes suficiente dinero para completar la compra.');
        return;
      }
      this.data_matches.forEach(match => {
        const catalogMatch = this.catalog_matches.find(m => m.id === match.id);
        if (catalogMatch) {
          catalogMatch.available -= match.quantity;
        }
      });
      this.balance -= totalCost;
      this.data_matches = [];
      alert('Compra finalizada');
      this.toggleBasket();
    },
    toggleBasket () {
      this.basketVisible = !this.basketVisible;
    },
    addToCart (match) {
      const existingMatch = this.data_matches.find(item => item.id === match.id);
      if (existingMatch) {
        existingMatch.quantity++;
      } else {
        this.data_matches.push({
          id: match.id,
          competition_id: this.getCompetitionId(match.competition),
          local: match.teams.split(' vs ')[0],
          visitor: match.teams.split(' vs ')[1],
          quantity: 1,
          price: match.price,
          sport: match.sport,
          competition: match.competition
        });
      }
    },
    getCompetitionId (competitionName) {
      const competition = this.data_competitions.find(c => c.name === competitionName);
      return competition ? competition.id : null;
    },
    closeBasket(){
      this.basketVisible = false;
    },
    login () {
      if (this.isLoggedIn) {
        this.isLoggedIn = false;
        this.closeBasket();
        this.removeAllItems();
      } else {
        //this.$router.push('/login');
        this.isLoggedIn = true;
      }
    },
    addBalance () {
      if (this.balanceInput > 0) {
        this.balance += parseFloat(this.balanceInput);
        this.balanceInput = 0;
        this.showBalanceInput = false;
      } else {
        alert('Por favor, ingrese una cantidad válida.');
      }
    }
  }
}
</script>


<style scoped>
.app {
}

.header {
  position: relative;
  background-color: #f2f2f2;
  padding: 20px;
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin: 40px auto;
  max-width: calc(100% - 60px);
}

.title {
  margin-left: 90px;
  font-size: 40px;
  color: #333;
  font-weight: bold;
  margin-right: auto;
}

.user-info {
  display: flex;
  align-items: center;
  margin-right: 25px;
}

.user-icon {
  font-size: 24px;
  margin-right: 5px;
}

.username {
  font-size: 16px;
  margin-right: 10px;
}

.balance {
  background-color: transparent;
  color: black;
  border: 1px solid black;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-left: 10px;
  transition: color 0.3s ease, transform 0.3s ease;
}

.balance:hover {
  transform: scale(1.1);
  background-color:transparent;
}

.balance-input {
  margin-left: 10px;
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 80px;
}

.close-basket {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 17px;
  cursor: pointer;
  margin-right: 120px;
  display: flex;
  align-items: center;
}

.close-basket:hover {
  background-color: #0056b3;
}

.increment,
.finalize {
  background-color: #00a600;
  color: white;
  border-radius: 2px;
}

.increment:hover,
.finalize:hover {
  background-color: #007f00;
}

.decrement {
  background-color: #ff0000;
  color: white;
  border-radius: 2px;
}

.decrement:hover {
  background-color: #b40303;
}

table {
  width: 100%;
  border-collapse: collapse;
}

.container {
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
  margin: 40px auto;
  max-width: calc(100% - 120px);
  padding: 50px;
  vertical-align: middle;
  text-align: center;
}

h2 {
  margin-bottom: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 2px;
}

th {
  background-color: #f2f2f2;
  text-align: center;
}

button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

button:hover {
  background-color: #b40303;
}

.back {
  margin: 5px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #808080;
}

.back:hover {
  background-color: #a9a9a9;
}

.actions {
  margin-top: 20px;
}

.back,
.finalize {
  margin: 5px;
  padding: 10px 20px;
  font-size: 16px;
}

.match-card {
  display: inline-block;
  width: 30%;
  margin: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  text-align: left;
  vertical-align: top;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.match-image {
  width: 100%;
  border-bottom: 1px solid #ddd;
}

.match-info {
  padding: 10px;
}

.add-to-cart {
  display: block;
  width: 100%;
  background-color: #28a745;
  color: white;
  padding: 10px;
  text-align: center;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.add-to-cart:hover {
  background-color: #218838;
}

.login-btn {
  position: absolute;
  top: 50px;
  right: 20px;
  background-color: #28a745;
  color: white;
  border: none;
  padding: 11px 20px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.login-btn:hover {
  background-color: #218838;
}

.match-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.cart-count {
  background-color: #007bff;
  color: white;
  border-radius: 50%;
  padding: 3px 10px;
  margin-left: 10px;
  font-size: 16px;
  border: 1px solid white;
  border-radius: 20px;
}
</style>

