import { Component, ViewChild, ElementRef } from '@angular/core';
import { Chart, registerables } from 'chart.js';
import { MilkService } from 'src/services/dairy/milk.services';

@Component({
  selector: 'milk-production-weekly-chart',
  templateUrl: './milk-production-weekly-chart.component.html',
  styleUrls: ['./milk-production-weekly-chart.component.css']
})
export class MilkProductionWeeklyChartComponent {
  @ViewChild('canvas') canvas!: ElementRef;
  chart!: Chart;
  data!: any[];

  constructor(private milkService: MilkService) { 
    Chart.register(...registerables);
  }

  ngOnInit(): void {
    this.milkService.getWeeklyMilkChartData().subscribe((data) => {
      this.data = data;
      this.createChart();
    });
  };

  createChart() {
    const chartData = {
      labels: this.data.map(item => item.day),
      datasets: [
        {
          label: 'Amount of Milk (Kgs)',
          data: this.data.map(item => {
            let totalMilk = 0;
            item.milk_records.forEach((record: { total_milk: number; }) => {
              totalMilk += record.total_milk;
            });
            return totalMilk;
          }),
          fill: true,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.3,
          borderWidth: 2.5
        }
      ]
    };
  
    const myChart = new Chart(this.canvas.nativeElement, {
      type: 'line',
      data: chartData,
      options: {
        responsive: true,
      scales: {
        y: {
          title: {
            display: true,
            text: 'Total Milk (Kgs)',
            font: {
              size: 12,
              weight: 'bold'
            }
          },
        },
        x: {
          title: {
            display: true,
            text: 'Days',
            font: {
              size: 16,
              weight: 'bold'
            }
          },
          ticks: {
            font: {
              size: 14
            }
          }
        }
      },
      plugins: {
        legend: {
          display: true,
          labels: {
            font: {
              size: 14
            }
          }
        }
      }
    }

    });
  }
};
