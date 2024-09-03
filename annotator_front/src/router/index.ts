import {createRouter, createWebHistory} from 'vue-router'
import Login from '@/views/Login.vue'
import { usePermissStore } from '@/store/permiss';
const routes = [
    {
        path: '/login',
        component: Login,
        meta: {
            title: "标注平台登录页"
        }
    },
    {
        path: '/403',
        component: () => import("@/views/403.vue"),
        meta: {
            title: "没有权限"
        }
    },
    {
        path: '/',
        redirect: '/WelcomeIndex',
    },
    {
        path: '/',
        component: () => import("@/views/home.vue"),
        children: [
            {
                path: '/WelcomeIndex',
                component: () => import("@/views/WelcomeIndex.vue"),
                meta: {
                    title: "首页",
                    permiss: '1'
                }
            },
            {
                path: '/DataSet',
                component: () => import("@/views/admin/DataSet.vue"),
                meta: {
                    title: "数据集",
                    permiss: '2'
                }
            },
            {
                path: '/View',
                component: () => import("@/views/View.vue"),
                meta: {
                    title: "数据集",
                    permiss: '3'
                }
            },
            {
                path: '/Fire',
                component: () => import("@/views/Fire.vue"),
                meta: {
                    title: "火柴人",
                    permiss: '6'
                }
            },
            {
                path: '/ViewTask',
                component: () => import("@/views/admin/ViewTask.vue"),
                meta: {
                    title: "查看任务",
                    permiss: '5'
                }
            },
            {
                path: '/WorkerInformation',
                component: () => import("@/views/worker/WorkerInformation.vue"),
                meta: {
                    title: "标注人员",
                    permiss: '4'
                }
            }
        ]
    },

];

const router = createRouter({
    // 4. 采用hash 模式
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title}`;
    const role = localStorage.getItem('userName');
    const userId = localStorage.getItem('userId');

    console.log(role)
    console.log(userId);
    
    const permiss = usePermissStore();
    if (!role && to.path !== '/login') {
        next('/login');
    } else if (to.meta.permiss && !permiss.key.includes(to.meta.permiss)) {
        next('/403');
    } else {
        next();
    }
});
export default router
