import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LillyComponent } from './lilly.component';

describe('LillyComponent', () => {
  let component: LillyComponent;
  let fixture: ComponentFixture<LillyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LillyComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LillyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
