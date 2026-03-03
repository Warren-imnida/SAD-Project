import { AfterViewInit, Component } from '@angular/core';
import { Chart } from 'chart.js/auto';

@Component({
  selector: 'app-dashboard',
  imports: [],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard implements AfterViewInit {
  chart: Chart | undefined;

  ngAfterViewInit() {
    const charts = [
      {
        id: 'myChart1',
        type: 'line',
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        data: [120, 190, 150, 210, 180, 140, 200],
        fill: true,
        color: 'rgba(37, 99, 235, 0.25)'
      },
      {
        id: 'myChart2',
        type: 'line',
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        data: [68, 72, 64, 78],
        fill: true,
        color: 'rgba(14, 165, 233, 0.25)'
      },
      {
        id: 'myChart3',
        type: 'bar',
        labels: ['MIS', 'Library', 'Dormitory'],
        data: [320, 420, 280],
        fill: false,
        color: 'rgba(34, 197, 94, 0.35)'
      },
      {
        id: 'myChart4',
        type: 'line',
        labels: ['2d', '3d', '4d', '5d', '6d'],
        data: [4.2, 3.8, 4.5, 3.2, 2.9],
        fill: true,
        color: 'rgba(248, 113, 113, 0.25)'
      }
    ];

    charts.forEach((chartConfig) => {
      const ctx = document.getElementById(chartConfig.id) as HTMLCanvasElement | null;

      if (!ctx) {
        return;
      }

      this.chart = new Chart(ctx, {
        type: chartConfig.type as any,
        data: {
          labels: chartConfig.labels,
          datasets: [
            {
              label: '',
              data: chartConfig.data,
              fill: chartConfig.fill || false,
              backgroundColor: chartConfig.color,
              borderColor: 'rgba(37, 99, 235, 0.9)',
              tension: 0.35,
              borderRadius: 8
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              ticks: {
                color: '#64748b'
              },
              grid: {
                color: 'rgba(148, 163, 184, 0.2)'
              }
            },
            x: {
              ticks: {
                color: '#64748b'
              },
              grid: {
                display: false
              }
            }
          }
        }
      });
    });
  }
}
