import { Component, AfterViewInit } from '@angular/core';
import { Chart } from 'chart.js/auto';




@Component({
  selector: 'app-dashboard',
  imports: [],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})

export class Dashboard implements AfterViewInit{
  chart: any; 
  ngAfterViewInit() {

    const charts = [
      { id: 'myChart1', type: 'line', data: [12, 19, 3, 5, 2], fill: true},
      { id: 'myChart2', type: 'line', data: [5, 10, 8, 3, 7], fill: true},
      { id: 'myChart3', type: 'line', data: [7, 2, 12, 5, 9], fill: true },
      { id: 'myChart4', type: 'line', data: [10, 20, 30, 40, 50], fill: true}
    ];

    charts.forEach(chartConfig => {
      const ctx = document.getElementById(chartConfig.id) as HTMLCanvasElement;

      this.chart = new Chart(ctx, {
        type: chartConfig.type as any,
        data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
          datasets: [{
            label:'',
            data: chartConfig.data,
            fill: chartConfig.fill || false,
            backgroundColor: 'rgba(14, 145, 21, 0.3)',
            borderColor: 'rgba(89, 192, 75, 1)',
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false 
        }
      }
    }
  });
        
  });      
}
}
