import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TotalPregnantCowsComponent } from './total-pregnant-cows.component';

describe('TotalPregnantCowsComponent', () => {
  let component: TotalPregnantCowsComponent;
  let fixture: ComponentFixture<TotalPregnantCowsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TotalPregnantCowsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TotalPregnantCowsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
