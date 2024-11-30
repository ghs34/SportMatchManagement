import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import TeamSet from '@/components/TeamSet'
import Cart from '@/components/Cart'
import Login from '@/components/Login'
import CreateAccount from '@/components/CreateAccount'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Cart',
      component: Cart

    },
    {
      path: '/teams',
      name: 'TeamSet',
      component: TeamSet
    },
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/LogIn',
      name: 'LogIn',
      component: Login
    },
    {
      path: '/CreateAccount',
      name: 'CreateAccount',
      component: CreateAccount
    }
  ]
})
