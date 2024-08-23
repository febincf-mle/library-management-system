import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue';
import BooksView from '../views/BooksView.vue';
import BookView from '../views/BookView.vue';
import AdminView from '../views/AdminView.vue';
import SectionView from "../views/SectionView.vue";
import SectionControlView from '../views/SectionControlView.vue';
import RentControlsView from '../views/RentControlsView.vue';
import RentedBooksView from '../views/RentedBooksView.vue';
import UserRentedBookView from '../views/UserRentedBookView.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/books',
      name: 'books',
      component: BooksView
    },
    {
      path: '/books/:id',
      name: 'book',
      component: BookView
    },
    {
      path: '/rented',
      name: 'rented',
      component: UserRentedBookView
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      children: [
        {
          path: 'rented-books',
          name: 'rented-books',
          component: RentedBooksView
        },
        {
        path: 'available-sections',
        name: 'sections',
        component: SectionView
      },
      {
        path: 'books',
        name: 'admin__books',
        component: BooksView
      },
      {
        path: '',
        name: 'admin-default',
        component: RentControlsView
      }
    ]
    },
    {
      path: '/admin/section/:id',
      name: 'sectioncontrols',
      component: SectionControlView
    },
    {
      path: '/sections',
      name: 'section-home',
      component: SectionView
    }
  ]
})

export default router;
