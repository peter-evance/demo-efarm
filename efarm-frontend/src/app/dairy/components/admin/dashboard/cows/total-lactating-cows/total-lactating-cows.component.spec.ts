import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TotalLactatingCowsComponent } from './total-lactating-cows.component';

describe('TotalLactatingCowsComponent', () => {
  let component: TotalLactatingCowsComponent;
  let fixture: ComponentFixture<TotalLactatingCowsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TotalLactatingCowsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TotalLactatingCowsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
