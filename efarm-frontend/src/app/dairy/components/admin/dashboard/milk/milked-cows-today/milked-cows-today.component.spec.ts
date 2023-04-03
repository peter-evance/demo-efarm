import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MilkedCowsTodayComponent } from './milked-cows-today.component';

describe('MilkedCowsTodayComponent', () => {
  let component: MilkedCowsTodayComponent;
  let fixture: ComponentFixture<MilkedCowsTodayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MilkedCowsTodayComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MilkedCowsTodayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
