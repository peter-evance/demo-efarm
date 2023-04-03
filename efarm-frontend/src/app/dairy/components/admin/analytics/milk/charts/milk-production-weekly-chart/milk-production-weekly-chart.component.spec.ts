import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MilkProductionWeeklyChartComponent } from './milk-production-weekly-chart.component';

describe('MilkProductionWeeklyChartComponent', () => {
  let component: MilkProductionWeeklyChartComponent;
  let fixture: ComponentFixture<MilkProductionWeeklyChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MilkProductionWeeklyChartComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MilkProductionWeeklyChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
