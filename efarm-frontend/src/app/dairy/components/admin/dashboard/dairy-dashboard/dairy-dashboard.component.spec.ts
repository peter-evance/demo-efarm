import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyDashboardComponent } from './dairy-dashboard.component';

describe('DairyDashboardComponent', () => {
  let component: DairyDashboardComponent;
  let fixture: ComponentFixture<DairyDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyDashboardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
