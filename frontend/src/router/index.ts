import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import NotFound from "../views/NotFoundView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/index",
      name: "index",
      component: HomeView,
    },
    {
      path: "/404",
      name: "notfound",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: NotFound,
    },
  ],
});

const whiltList = ["/", "/404"];

router.beforeEach((to, from, next) => {
  //whitelist
  if (whiltList.includes(to.path)) {
    next();
  } else {
    next({
      path: "/404",
    });
  }
});
export default router;
