import { Routes } from '@angular/router';
import { Dashboard } from './dashboard/dashboard';
import { FirstPage } from './login-page/first-page/first-page';

export const routes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: FirstPage},
  { path: 'dashboard', component: Dashboard },
];
